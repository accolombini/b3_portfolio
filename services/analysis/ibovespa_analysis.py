"""
Sessão 01 — IBOVESPA + Comparação com Carteira Atual
======================================================
Módulo exploratório que:
 1. Busca histórico real do IBOVESPA (^BVSP) via yfinance
 2. Projeta IBOVESPA para 2 anos via ARIMA (pmdarima auto_arima)
 3. Busca dados reais dos 3 ativos da carteira (CVM, Tesouro, BCB)
 4. Normaliza todas as séries em base 100 para comparação
 5. Gera gráfico comparativo com matplotlib

Regras absolutas (CLAUDE.md):
 - NUNCA simular dados
 - NUNCA hardcodar valores financeiros
 - NUNCA assumir API disponível sem testar
 - Sempre usar a próxima fonte da cadeia se a atual falhar
 - Registrar em log fonte usada e período obtido
"""

from __future__ import annotations

import io
import zipfile
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import matplotlib

matplotlib.use("Agg")  # sem display — compatível com servidor
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import structlog
import yfinance as yf

# ---------------------------------------------------------------------------
# Logger
# ---------------------------------------------------------------------------
log = structlog.get_logger(__name__)


# ---------------------------------------------------------------------------
# 1. IBOVESPA histórico
# ---------------------------------------------------------------------------


def fetch_ibovespa_history(years: int = 5) -> pd.DataFrame:
    """
    Busca histórico do IBOVESPA (^BVSP) via yfinance.

    Args:
        years: Quantidade de anos de histórico desejado (padrão: 5).

    Returns:
        DataFrame com colunas: Date, Close, Daily_Return
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=years * 365)

    log.info(
        "fetch_ibovespa_history.start",
        ticker="^BVSP",
        start=str(start_date),
        end=str(end_date),
    )

    ticker = yf.Ticker("^BVSP")
    raw: pd.DataFrame = ticker.history(
        start=start_date.strftime("%Y-%m-%d"),
        end=end_date.strftime("%Y-%m-%d"),
        auto_adjust=True,
    )

    if raw.empty:
        raise RuntimeError("yfinance retornou DataFrame vazio para ^BVSP")

    # Normalizar índice → coluna Date
    df = raw[["Close"]].copy()
    df.index = pd.to_datetime(df.index)
    df.index = df.index.tz_localize(None) if df.index.tz is not None else df.index
    df = df.reset_index().rename(columns={"index": "Date", "Datetime": "Date"})
    if "Date" not in df.columns and df.columns[0] != "Date":
        first_col = str(df.columns[0])
        df = df.rename(columns={first_col: "Date"})

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    df["Daily_Return"] = df["Close"].pct_change()

    periodo_real = df["Date"].max() - df["Date"].min()
    dias_esperados = years * 365
    if periodo_real.days < dias_esperados:
        log.warning(
            "fetch_ibovespa_history.periodo_menor_que_esperado",
            periodo_obtido_dias=periodo_real.days,
            periodo_esperado_dias=dias_esperados,
            data_inicial=str(df["Date"].min().date()),
            data_final=str(df["Date"].max().date()),
        )
    else:
        log.info(
            "fetch_ibovespa_history.ok",
            registros=len(df),
            data_inicial=str(df["Date"].min().date()),
            data_final=str(df["Date"].max().date()),
        )

    return pd.DataFrame(df[["Date", "Close", "Daily_Return"]])


# ---------------------------------------------------------------------------
# 2. Projeção ARIMA
# ---------------------------------------------------------------------------


def project_ibovespa(
    historical_df: pd.DataFrame,
    n_periods: int = 504,
) -> pd.DataFrame:
    """
    Projeta o IBOVESPA para n_periods dias úteis usando ARIMA.

    Tenta auto_arima (pmdarima) para seleção automática de parâmetros.
    Se falhar, usa ARIMA(1,1,1) documentando a escolha.

    Args:
        historical_df: DataFrame retornado por fetch_ibovespa_history().
        n_periods: Dias úteis de projeção (~504 = 2 anos). Default: 504.

    Returns:
        DataFrame com colunas: Date, Projected_Close, CI_Lower_95, CI_Upper_95
    """
    close: pd.Series = pd.Series(historical_df.set_index("Date")["Close"].dropna().sort_index())

    # Trabalhar em log para garantir positividade e melhor estacionaridade
    log_close = np.log(close)

    forecast_log = None
    conf_int_log = None

    # --- Tentativa 1: pmdarima auto_arima para seleção automática de ordem ---
    try:
        from pmdarima import auto_arima

        log.info("project_ibovespa.tentando_auto_arima")
        model_pm = auto_arima(
            log_close.values,  # array puro — evita problemas de índice com sklearn
            seasonal=False,
            suppress_warnings=True,
            error_action="ignore",
            stepwise=True,
            information_criterion="aic",
            max_p=3,
            max_q=3,
            max_d=2,
        )
        order_used = model_pm.order
        log.info("project_ibovespa.auto_arima_order_selecionado", order=order_used)

        forecast_log, conf_int_log = model_pm.predict(
            n_periods=n_periods,
            return_conf_int=True,
            alpha=0.05,
        )
    except ImportError:
        log.warning(
            "project_ibovespa.pmdarima_nao_instalado",
            mensagem="pmdarima não disponível — usando ARIMA(1,1,1) via statsmodels",
        )
    except Exception as e:
        log.warning(
            "project_ibovespa.auto_arima_falhou",
            erro=str(e),
            mensagem="auto_arima falhou (possivelmente incompatibilidade "
            "pmdarima/sklearn) — usando ARIMA(1,1,1) via statsmodels",
        )

    # --- Fallback: statsmodels ARIMA(1,1,1) ---
    if forecast_log is None:
        from statsmodels.tsa.arima.model import ARIMA as SM_ARIMA

        log.info("project_ibovespa.usando_statsmodels_arima_111")
        sm_model = SM_ARIMA(log_close, order=(1, 1, 1)).fit()
        return _project_with_statsmodels(sm_model, close, n_periods)

    projected_close = np.exp(forecast_log)
    assert conf_int_log is not None
    ci_lower = np.exp(conf_int_log[:, 0])
    ci_upper = np.exp(conf_int_log[:, 1])

    # Gerar datas futuras (dias úteis)
    last_date = pd.Timestamp(str(close.index.max()))
    future_dates = pd.bdate_range(
        start=last_date + pd.Timedelta(days=1),
        periods=n_periods,
    )

    result = pd.DataFrame(
        {
            "Date": future_dates,
            "Projected_Close": projected_close,
            "CI_Lower_95": ci_lower,
            "CI_Upper_95": ci_upper,
        }
    )

    log.info(
        "project_ibovespa.ok",
        periodos=n_periods,
        data_inicio_projecao=str(result["Date"].iloc[0].date()),
        data_fim_projecao=str(result["Date"].iloc[-1].date()),
    )
    return result


def _project_with_statsmodels(
    model,
    close: pd.Series,
    n_periods: int,
) -> pd.DataFrame:
    """Fallback: projeção com modelo statsmodels já ajustado."""
    forecast_result = model.get_forecast(steps=n_periods)
    summary = forecast_result.summary_frame(alpha=0.05)

    projected_close = np.exp(summary["mean"].values)
    ci_lower = np.exp(summary["mean_ci_lower"].values)
    ci_upper = np.exp(summary["mean_ci_upper"].values)

    last_date = pd.Timestamp(str(close.index.max()))
    future_dates = pd.bdate_range(
        start=last_date + pd.Timedelta(days=1),
        periods=n_periods,
    )

    return pd.DataFrame(
        {
            "Date": future_dates[: len(projected_close)],
            "Projected_Close": projected_close,
            "CI_Lower_95": ci_lower,
            "CI_Upper_95": ci_upper,
        }
    )


# ---------------------------------------------------------------------------
# 3. Fontes auxiliares — BCB
# ---------------------------------------------------------------------------


def _fetch_bcb_series(series_id: int, start_date: Optional[str] = None) -> pd.DataFrame:
    """
    Busca série temporal do Banco Central do Brasil (SGS/BCB).

    O BCB aceita no máximo 10 anos de janela para séries diárias.
    Por padrão usa 9 anos atrás da data atual (margem de segurança).

    Args:
        series_id: Código da série (ex: 12=CDI, 432=SELIC).
        start_date: Data inicial no formato DD/MM/AAAA.
                    Default: 9 anos atrás de hoje.

    Returns:
        DataFrame com colunas Date e Rate (em % ao dia).

    Raises:
        requests.HTTPError: Se a API retornar erro HTTP.
        RuntimeError: Se o response estiver vazio.
    """
    if start_date is None:
        five_years_ago = date.today() - timedelta(days=5 * 365)
        start_date = five_years_ago.strftime("%d/%m/%Y")
    today = date.today().strftime("%d/%m/%Y")
    url = (
        f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{series_id}/dados"
        f"?formato=json&dataInicial={start_date}&dataFinal={today}"
    )
    log.info("_fetch_bcb_series.request", series_id=series_id, url=url)

    resp = requests.get(
        url,
        timeout=90,
        headers={
            "Accept": "application/json",
            "User-Agent": "b3-portfolio-analysis/1.0 (educational; non-commercial)",
        },
    )
    resp.raise_for_status()
    data = resp.json()

    if not data:
        raise RuntimeError(f"BCB série {series_id}: response vazio")

    df = pd.DataFrame(data)
    df["Date"] = pd.to_datetime(df["data"], dayfirst=True)
    df["Rate"] = pd.to_numeric(df["valor"], errors="coerce")
    df = pd.DataFrame(df[["Date", "Rate"]].dropna()).sort_values("Date").reset_index(drop=True)

    log.info(
        "_fetch_bcb_series.ok",
        series_id=series_id,
        registros=len(df),
        data_inicial=str(df["Date"].min().date()),
        data_final=str(df["Date"].max().date()),
    )
    return df


def _accumulate_rate_to_index(
    rate_df: pd.DataFrame,
    start_value: float = 100.0,
    rate_type: str = "daily_pct",
) -> pd.DataFrame:
    """
    Transforma série de taxas (%) em índice acumulado.

    Args:
        rate_df: DataFrame com colunas Date e Rate.
        start_value: Valor inicial do índice. Default: 100.0.
        rate_type: Escala da taxa recebida.
            "daily_pct"  — % ao dia (ex: 0.047 = 0,047%/dia). BCB série 12 (CDI).
                           Fator diário: 1 + rate/100
            "annual_pct" — % ao ano (ex: 13.75 = 13,75% a.a.). BCB série 432 (SELIC).
                           Converte para diário: (1 + rate/100)^(1/252) - 1

    Returns:
        DataFrame com colunas Date e Value (índice acumulado, começa em start_value).

    Raises:
        ValueError: Se rate_type for diferente de "daily_pct" ou "annual_pct".
    """
    if rate_type not in ("daily_pct", "annual_pct"):
        raise ValueError(
            f"rate_type inválido: '{rate_type}'. "
            "Use 'daily_pct' (BCB série 12 — CDI) ou 'annual_pct' (BCB série 432 — SELIC)."
        )

    df = rate_df.copy().sort_values("Date").reset_index(drop=True)

    if rate_type == "daily_pct":
        # BCB série 12 (CDI): taxa em % ao dia, ex: 0.047 → fator 1.00047
        factors = np.array(1 + df["Rate"] / 100, dtype=float)
    else:
        # BCB série 432 (SELIC): taxa em % ao ano, ex: 13.75 → converter para diário
        # taxa_diaria = (1 + 13.75/100)^(1/252) - 1
        factors = np.array((1 + df["Rate"] / 100) ** (1 / 252), dtype=float)

    index_values = np.cumprod(factors) / factors[0] * start_value

    df["Value"] = index_values
    return pd.DataFrame(df[["Date", "Value"]])


# ---------------------------------------------------------------------------
# 4. Busca de ativos da carteira
# ---------------------------------------------------------------------------


def _fetch_rf_lp_high() -> Dict[str, Any]:
    """
    Ativo 1: Fundos de Investimento RF LP High.
    Cadeia: CVM Dados Abertos → CDI (BCB série 12).
    """
    # --- Tentativa 1: CVM Dados Abertos ---
    try:
        log.info("_fetch_rf_lp_high.tentando_cvm")
        # Arquivo de cadastro atual: cad_fi.csv
        cad_url = "https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv"
        resp = requests.get(cad_url, timeout=60)
        resp.raise_for_status()

        # CVM usa encoding latin-1 (ISO-8859-1)
        cad_df = pd.read_csv(
            io.StringIO(resp.content.decode("latin-1")),
            sep=";",
            dtype=str,
            low_memory=False,
        )

        # Buscar por nome do fundo
        search_terms = ["RF LP HIGH", "RENDA FIXA LP HIGH", "RF LP HI"]
        mask = pd.Series(False, index=cad_df.index)
        for term in search_terms:
            mask |= (
                cad_df["DENOM_SOCIAL"]
                .str.upper()
                .str.contains(term, na=False, regex=False)
            )

        found = cad_df[mask]
        if found.empty:
            log.warning(
                "_fetch_rf_lp_high.nao_localizado_cvm",
                mensagem="Fundo RF LP High não localizado na CVM por nome — "
                "necessário fornecer CNPJ manualmente",
                termos_buscados=search_terms,
            )
            raise ValueError("RF LP High não encontrado na CVM por nome")

        # Pegar o primeiro resultado (pode haver mais de um fundo com nome similar)
        cnpj = found.iloc[0]["CNPJ_FUNDO"].strip()
        nome_encontrado = found.iloc[0]["DENOM_SOCIAL"].strip()
        log.info(
            "_fetch_rf_lp_high.cvm_fundo_encontrado",
            cnpj=cnpj,
            nome=nome_encontrado,
            total_fundos_encontrados=len(found),
        )

        # Baixar cotas mensais dos últimos 5 anos
        end_year = date.today().year
        end_month = date.today().month
        frames = []
        failures = []

        for delta_months in range(0, 60):  # até 60 meses = 5 anos
            y = end_year - (delta_months + end_month - 1) // 12
            m = (end_month - 1 - delta_months % 12) % 12 + 1
            # Calcular mês correto
            total_months = end_year * 12 + end_month - 1 - delta_months
            y = total_months // 12
            m = total_months % 12 + 1
            ym = f"{y:04d}{m:02d}"
            # Arquivos mensais disponíveis como .zip (contêm CSV interno)
            url_cota = (
                f"https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/"
                f"inf_diario_fi_{ym}.zip"
            )
            try:
                r = requests.get(url_cota, timeout=60)
                r.raise_for_status()
                with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
                    csv_name = zf.namelist()[0]
                    with zf.open(csv_name) as f:
                        monthly = pd.read_csv(
                            io.TextIOWrapper(f, encoding="latin-1"),
                            sep=";",
                            dtype=str,
                            low_memory=False,
                        )
                filtered = monthly[monthly["CNPJ_FUNDO"].str.strip() == cnpj]
                if not filtered.empty:
                    filtered = filtered[["DT_COMPTC", "VL_QUOTA"]].copy()
                    filtered["Date"] = pd.to_datetime(filtered["DT_COMPTC"])
                    filtered["Value"] = pd.to_numeric(
                        filtered["VL_QUOTA"].str.replace(",", "."),
                        errors="coerce",
                    )
                    frames.append(filtered[["Date", "Value"]])
            except Exception as e:
                failures.append((ym, str(e)))

        if failures:
            log.warning(
                "_fetch_rf_lp_high.cvm_meses_falhos",
                meses_falhos=len(failures),
            )

        if not frames:
            raise ValueError(
                f"RF LP High (CNPJ={cnpj}) não retornou cotas — "
                "arquivos mensais CVM sem dados para este fundo."
            )

        data_df = (
            pd.concat(frames, ignore_index=True)
            .dropna()
            .sort_values("Date")
            .drop_duplicates("Date")
            .reset_index(drop=True)
        )
        period = f"{data_df['Date'].min().date()} → {data_df['Date'].max().date()}"
        log.info(
            "_fetch_rf_lp_high.cvm_ok",
            registros=len(data_df),
            period=period,
        )
        return {
            "data": data_df,
            "source": f"CVM Dados Abertos (CNPJ: {cnpj}, {nome_encontrado})",
            "period": period,
            "proxy_used": False,
        }

    except Exception as e:
        log.warning(
            "_fetch_rf_lp_high.cvm_falhou_usando_proxy_cdi",
            erro=str(e),
        )

    # --- Fallback: CDI acumulado (BCB série 12) ---
    log.info("_fetch_rf_lp_high.usando_proxy_cdi")
    cdi_df = _fetch_bcb_series(12)
    data_df = _accumulate_rate_to_index(cdi_df, rate_type="daily_pct")
    period = f"{data_df['Date'].min().date()} → {data_df['Date'].max().date()}"
    return {
        "data": data_df,
        "source": "Proxy: CDI acumulado (BCB série 12)",
        "period": period,
        "proxy_used": True,
    }


def _fetch_lft_2031() -> Dict[str, Any]:
    """
    Ativo 2: Tesouro Direto LFT 01.03.2031.
    Cadeia: API Tesouro gov.br → SELIC acumulada (BCB série 432).
    """
    # --- Tentativa 1: API Tesouro gov.br ---
    endpoints = [
        "https://www.tesourodireto.com.br/json/br/com/b3/tesourodireto/component/"
        "publicarea/PortfolioTesouroDiretoComponent/bd/bdTd.json",
        "https://apigtw.tesouro.gov.br/api/v1/titulos/precos-taxas",
    ]

    for endpoint in endpoints:
        try:
            log.info("_fetch_lft_2031.tentando_tesouro", endpoint=endpoint)
            resp = requests.get(endpoint, timeout=30)
            resp.raise_for_status()
            raw = resp.json()

            # O JSON do bdTd tem estrutura: TrsrBdTrad.TrsrBd (lista de títulos)
            # Navegar até os dados históricos de preços
            titulos = None
            if "TrsrBdTrad" in raw:
                titulos = raw["TrsrBdTrad"].get("TrsrBd", [])
            elif isinstance(raw, list):
                titulos = raw

            if not titulos:
                log.warning("_fetch_lft_2031.endpoint_sem_dados", endpoint=endpoint)
                continue

            # Buscar LFT
            lft_entries = []
            for t in titulos:
                nome = (
                    t.get("TrsrNm", "") or t.get("nm", "") or t.get("name", "") or ""
                ).upper()
                if "LFT" in nome or "SELIC" in nome or "TESOURO SELIC" in nome:
                    lft_entries.append(t)

            if not lft_entries:
                log.warning(
                    "_fetch_lft_2031.lft_nao_encontrado_no_endpoint",
                    endpoint=endpoint,
                )
                continue

            # Tentar extrair histórico de preços
            # A estrutura do bdTd não traz histórico — apenas preço atual
            # Verificar se há chave histórica
            rows = []
            for entry in lft_entries:
                hist = entry.get("TrsrBdPrice", []) or entry.get("prices", [])
                if hist:
                    for h in hist:
                        dt = h.get("prcDt") or h.get("date")
                        price = h.get("untrRedVal") or h.get("price")
                        if dt and price:
                            rows.append({"Date": dt, "Value": float(price)})

            if not rows:
                log.warning(
                    "_fetch_lft_2031.historico_nao_disponivel_no_endpoint",
                    endpoint=endpoint,
                )
                continue

            data_df = pd.DataFrame(rows)
            data_df["Date"] = pd.to_datetime(data_df["Date"])
            data_df = (
                data_df.dropna()
                .sort_values("Date")
                .drop_duplicates("Date")
                .reset_index(drop=True)
            )
            period = f"{data_df['Date'].min().date()} → {data_df['Date'].max().date()}"
            log.info(
                "_fetch_lft_2031.tesouro_ok",
                registros=len(data_df),
                period=period,
            )
            return {
                "data": data_df,
                "source": f"API Tesouro Direto ({endpoint})",
                "period": period,
                "proxy_used": False,
            }

        except Exception as e:
            log.warning(
                "_fetch_lft_2031.endpoint_falhou",
                endpoint=endpoint,
                erro=str(e),
            )

    # --- Fallback: SELIC acumulada (BCB série 432) ---
    log.warning(
        "_fetch_lft_2031.usando_proxy_selic",
        mensagem="Proxy utilizado: SELIC acumulada (BCB série 432). "
        "API Tesouro Direto não retornou histórico de preços.",
    )
    selic_df = _fetch_bcb_series(432)
    data_df = _accumulate_rate_to_index(selic_df, rate_type="annual_pct")
    period = f"{data_df['Date'].min().date()} → {data_df['Date'].max().date()}"
    return {
        "data": data_df,
        "source": "Proxy: SELIC acumulada (BCB série 432)",
        "period": period,
        "proxy_used": True,
    }


def _fetch_lca_bb_prefixada() -> Dict[str, Any]:
    """
    Ativo 3: LCA BB Prefixada.
    LCAs não possuem dados públicos de cota.
    Cadeia: ANBIMA IRF-M → CDI (BCB série 12).

    Registra limitação no log: LCA BB Prefixada não possui dados públicos
    de cota — proxy utilizado.
    """
    log.warning(
        "_fetch_lca_bb_prefixada.sem_dados_publicos",
        mensagem="LCA BB Prefixada não possui dados públicos de cota. "
        "Tentando proxy ANBIMA IRF-M, fallback CDI.",
    )

    # --- Tentativa 1: ANBIMA IRF-M ---
    try:
        log.info("_fetch_lca_bb_prefixada.tentando_anbima")
        # ANBIMA não tem API pública aberta sem autenticação para IRF-M histórico
        # Tentativa com o endpoint de carteiras de mercado
        anbima_url = (
            "https://api.anbima.com.br/feed/precos-v1/titulos-publicos/"
            "mercado-secundario-tpf/ult-dia-utl"
        )
        resp = requests.get(
            anbima_url, timeout=15, headers={"accept": "application/json"}
        )
        resp.raise_for_status()

        data = resp.json()
        # ANBIMA API pode exigir token — se chegar aqui, está ok
        rows = []
        if isinstance(data, list):
            for item in data:
                if "IRF-M" in str(item.get("titulo", "")).upper():
                    rows.append(
                        {
                            "Date": item.get("data_referencia"),
                            "Value": item.get("numero_indice"),
                        }
                    )

        if not rows:
            raise ValueError("ANBIMA não retornou dados de IRF-M acessíveis")

        data_df = pd.DataFrame(rows)
        data_df["Date"] = pd.to_datetime(data_df["Date"])
        data_df["Value"] = pd.to_numeric(data_df["Value"], errors="coerce")
        data_df = data_df.dropna().sort_values("Date").reset_index(drop=True)
        period = f"{data_df['Date'].min().date()} → {data_df['Date'].max().date()}"
        log.info(
            "_fetch_lca_bb_prefixada.anbima_ok",
            registros=len(data_df),
            period=period,
        )
        return {
            "data": data_df,
            "source": "Proxy: ANBIMA IRF-M (índice de renda fixa prefixada)",
            "period": period,
            "proxy_used": True,
        }

    except Exception as e:
        log.warning(
            "_fetch_lca_bb_prefixada.anbima_falhou",
            erro=str(e),
        )

    # --- Fallback final: CDI acumulado (BCB série 12) ---
    log.warning(
        "_fetch_lca_bb_prefixada.usando_proxy_cdi",
        mensagem="LCA BB Prefixada — proxy utilizado: CDI acumulado (BCB série 12). "
        "ANBIMA IRF-M não acessível sem autenticação.",
    )
    cdi_df = _fetch_bcb_series(12)
    data_df = _accumulate_rate_to_index(cdi_df, rate_type="daily_pct")
    period = f"{data_df['Date'].min().date()} → {data_df['Date'].max().date()}"
    return {
        "data": data_df,
        "source": "Proxy: CDI acumulado (BCB série 12) — "
        "LCA BB Prefixada sem dados públicos de cota",
        "period": period,
        "proxy_used": True,
    }


def fetch_portfolio_assets() -> Dict[str, Dict[str, Any]]:
    """
    Busca dados dos 3 ativos da carteira atual.

    Returns:
        Dicionário com chaves: rf_lp_high, lft_2031, lca_bb_prefixada.
        Cada valor é um dict com: data (DataFrame), source (str),
        period (str), proxy_used (bool).
    """
    log.info("fetch_portfolio_assets.start")

    assets = {}
    assets["rf_lp_high"] = _fetch_rf_lp_high()
    assets["lft_2031"] = _fetch_lft_2031()
    assets["lca_bb_prefixada"] = _fetch_lca_bb_prefixada()

    for key, val in assets.items():
        log.info(
            "fetch_portfolio_assets.ativo_resumo",
            ativo=key,
            source=val["source"],
            period=val["period"],
            proxy_used=val["proxy_used"],
            registros=len(val["data"]),
        )

    return assets


# ---------------------------------------------------------------------------
# 5. Normalização base 100
# ---------------------------------------------------------------------------


def normalize_series(df: pd.DataFrame, value_col: str) -> pd.DataFrame:
    """
    Normaliza uma série temporal para base 100 no primeiro valor disponível.

    Args:
        df: DataFrame com colunas Date e value_col.
        value_col: Nome da coluna de valores a normalizar.

    Returns:
        DataFrame com colunas Date, value_col e Normalized.

    Raises:
        ValueError: Se o primeiro valor for zero.
    """
    df = df.copy().sort_values("Date").reset_index(drop=True)
    non_null_values = df[value_col].dropna()
    if non_null_values.empty:
        raise ValueError(f"Coluna '{value_col}' não contém valores válidos")

    base_value = non_null_values.iloc[0]
    if base_value == 0:
        raise ValueError(
            f"Valor base zero na coluna '{value_col}' — normalização impossível"
        )

    df["Normalized"] = (df[value_col] / base_value) * 100.0
    return df


# ---------------------------------------------------------------------------
# 6. Gráfico comparativo
# ---------------------------------------------------------------------------


def generate_comparison_chart(
    ibov_df: pd.DataFrame,
    projection_df: pd.DataFrame,
    assets: Dict[str, Dict[str, Any]],
    output_path: Optional[str] = None,
) -> str:
    """
    Gera gráfico comparativo com 2 subplots:
      - Subplot 1: histórico IBOVESPA + 3 ativos (normalizados base 100)
      - Subplot 2: projeção IBOVESPA 2 anos com IC 95%

    Args:
        ibov_df: DataFrame de fetch_ibovespa_history().
        projection_df: DataFrame de project_ibovespa().
        assets: Dict de fetch_portfolio_assets().
        output_path: Caminho de saída. Default: services/analysis/outputs/...

    Returns:
        Caminho absoluto do arquivo PNG gerado.
    """
    if output_path is None:
        base_dir = Path(__file__).parent / "outputs"
        output_path = str(base_dir / "ibovespa_comparison.png")

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(2, 1, figsize=(14, 12))
    fig.suptitle(
        "IBOVESPA vs Carteira Atual — Análise Exploratória\n"
        f"(Gerado em {date.today().strftime('%d/%m/%Y')})",
        fontsize=14,
        fontweight="bold",
    )

    # -----------------------------------------------------------------------
    # Subplot 1 — Histórico normalizado
    # -----------------------------------------------------------------------
    ax1 = axes[0]

    # IBOVESPA normalizado
    ibov_norm = normalize_series(ibov_df.rename(columns={"Close": "Value"}), "Value")
    ax1.plot(
        ibov_norm["Date"],
        ibov_norm["Normalized"],
        label="IBOVESPA (^BVSP)",
        linewidth=2,
        color="navy",
    )

    # Cores para os ativos da carteira
    asset_colors = {
        "rf_lp_high": "forestgreen",
        "lft_2031": "darkorange",
        "lca_bb_prefixada": "crimson",
    }
    asset_labels = {
        "rf_lp_high": "FI RF LP High",
        "lft_2031": "LFT 2031",
        "lca_bb_prefixada": "LCA BB Prefixada",
    }

    for key, asset in assets.items():
        data = asset["data"].copy()
        label_base = asset_labels.get(key, key)
        proxy = asset["proxy_used"]
        source_short = asset["source"].replace("Proxy: ", "").split(" (")[0]

        if proxy:
            label = f"{label_base}\n(proxy: {source_short})"
        else:
            label = label_base

        # Normalizar a partir da data base comum com IBOVESPA
        common_start = ibov_norm["Date"].min()
        data_from_common = data[data["Date"] >= common_start].copy()

        if len(data_from_common) > 0:
            data_norm = normalize_series(data_from_common, "Value")
        else:
            # Série mais curta — normalizar a partir do próprio início
            data_norm = normalize_series(data, "Value")
            log.info(
                "generate_comparison_chart.ativo_normalizado_proprio_inicio",
                ativo=key,
                data_base=str(data_norm["Date"].iloc[0].date()),
            )

        ax1.plot(
            data_norm["Date"],
            data_norm["Normalized"],
            label=label,
            linewidth=1.8,
            linestyle="--" if proxy else "-",
            color=asset_colors.get(key, "gray"),
        )

    ax1.set_title("Histórico — Base 100 na data inicial do IBOVESPA", fontsize=11)
    ax1.set_ylabel("Índice (Base 100)")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax1.xaxis.set_major_locator(mdates.YearLocator())
    ax1.legend(fontsize=8, loc="upper left")
    ax1.grid(alpha=0.3)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)

    # -----------------------------------------------------------------------
    # Subplot 2 — Projeção IBOVESPA
    # -----------------------------------------------------------------------
    ax2 = axes[1]

    # Últimos 252 dias históricos para contexto
    ibov_recent = ibov_norm.tail(252)
    ax2.plot(
        ibov_recent["Date"],
        ibov_recent["Normalized"],
        label="IBOVESPA histórico (1 ano)",
        linewidth=2,
        color="navy",
    )

    # Normalizar projeção em relação ao último ponto histórico
    last_hist_close = ibov_df["Close"].dropna().iloc[-1]
    last_hist_norm = ibov_norm["Normalized"].iloc[-1]
    scale = last_hist_norm / last_hist_close

    proj_norm = projection_df["Projected_Close"] * scale
    ci_lower_norm = projection_df["CI_Lower_95"] * scale
    ci_upper_norm = projection_df["CI_Upper_95"] * scale

    ax2.plot(
        projection_df["Date"],
        proj_norm,
        label="Projeção ARIMA (2 anos)",
        linewidth=2,
        linestyle="--",
        color="darkorange",
    )
    ax2.fill_between(
        projection_df["Date"],
        ci_lower_norm,
        ci_upper_norm,
        alpha=0.2,
        color="darkorange",
        label="IC 95%",
    )

    ax2.set_title("Projeção IBOVESPA — ARIMA (2 anos)", fontsize=11)
    ax2.set_ylabel("Índice (Base 100)")
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%m/%Y"))
    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax2.legend(fontsize=9, loc="upper left")
    ax2.grid(alpha=0.3)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)

    plt.tight_layout()
    plt.savefig(str(output_file), dpi=150, bbox_inches="tight")
    plt.close(fig)

    log.info("generate_comparison_chart.ok", output_path=str(output_file))
    return str(output_file)


# ---------------------------------------------------------------------------
# Execução standalone
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import structlog

    structlog.configure(
        processors=[
            structlog.dev.ConsoleRenderer(),
        ]
    )

    print("=" * 60)
    print("Sessão 01 — IBOVESPA + Comparação com Carteira Atual")
    print("=" * 60)

    print("\n[1/4] Buscando histórico IBOVESPA...")
    ibov = fetch_ibovespa_history()
    print(
        f"  → {len(ibov)} registros | {ibov['Date'].min().date()} → {ibov['Date'].max().date()}"
    )

    print("\n[2/4] Projetando IBOVESPA (ARIMA, 2 anos)...")
    proj = project_ibovespa(ibov)
    print(
        f"  → {len(proj)} pontos | {proj['Date'].iloc[0].date()} → {proj['Date'].iloc[-1].date()}"
    )

    print("\n[3/4] Buscando ativos da carteira...")
    assets = fetch_portfolio_assets()
    for key, val in assets.items():
        proxy_tag = " [PROXY]" if val["proxy_used"] else ""
        print(f"  {key}:")
        print(f"    Fonte: {val['source']}{proxy_tag}")
        print(f"    Período: {val['period']}")
        print(f"    Registros: {len(val['data'])}")

    print("\n[4/4] Gerando gráfico comparativo...")
    output = generate_comparison_chart(ibov, proj, assets)
    print(f"  → Gráfico salvo em: {output}")

    print("\n✓ Sessão 01 concluída.")
