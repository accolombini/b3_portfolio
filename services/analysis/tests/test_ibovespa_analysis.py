"""
Testes TDD para ibovespa_analysis.py
Sessão 01 — IBOVESPA + Comparação com Carteira Atual

Regras:
- NUNCA mockar dados financeiros reais
- NUNCA hardcodar valores de cotação, taxa ou data
- Os testes validam estrutura, tipos e invariantes — não valores absolutos
"""

import sys
from pathlib import Path

# Garantir importação do módulo a ser testado
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import pytest

# ---------------------------------------------------------------------------
# 1. Busca histórica do IBOVESPA
# ---------------------------------------------------------------------------


class TestFetchIbovespa:
    """Testa a função fetch_ibovespa_history."""

    def test_retorna_dataframe(self):
        from ibovespa_analysis import fetch_ibovespa_history

        df = fetch_ibovespa_history()
        assert isinstance(df, pd.DataFrame), "Deve retornar um DataFrame"

    def test_colunas_obrigatorias(self):
        from ibovespa_analysis import fetch_ibovespa_history

        df = fetch_ibovespa_history()
        assert "Date" in df.columns, "Coluna 'Date' ausente"
        assert "Close" in df.columns, "Coluna 'Close' ausente"
        assert "Daily_Return" in df.columns, "Coluna 'Daily_Return' ausente"

    def test_dataframe_nao_vazio(self):
        from ibovespa_analysis import fetch_ibovespa_history

        df = fetch_ibovespa_history()
        assert len(df) > 0, "DataFrame não pode ser vazio"

    def test_close_positivo(self):
        from ibovespa_analysis import fetch_ibovespa_history

        df = fetch_ibovespa_history()
        assert (df["Close"].dropna() > 0).all(), "Close deve ser sempre positivo"

    def test_date_eh_datetime(self):
        from ibovespa_analysis import fetch_ibovespa_history

        df = fetch_ibovespa_history()
        # Date pode ser índice ou coluna; verificar que é datetime-like
        date_col = df["Date"]
        assert pd.api.types.is_datetime64_any_dtype(date_col) or hasattr(
            date_col.iloc[0], "year"
        ), "Coluna Date deve ser datetime"

    def test_periodo_maximo_5_anos(self):
        from ibovespa_analysis import fetch_ibovespa_history

        df = fetch_ibovespa_history()
        date_col = pd.to_datetime(df["Date"])
        delta = date_col.max() - date_col.min()
        # Deve ter pelo menos 1 ano de dados (IBOVESPA tem décadas de histórico)
        assert delta.days >= 365, f"Período muito curto: {delta.days} dias"

    def test_daily_return_eh_numerico(self):
        from ibovespa_analysis import fetch_ibovespa_history

        df = fetch_ibovespa_history()
        assert pd.api.types.is_float_dtype(
            df["Daily_Return"].dtype
        ) or pd.api.types.is_numeric_dtype(df["Daily_Return"].dtype), (
            "Daily_Return deve ser numérico"
        )

    def test_daily_return_primeira_linha_nan(self):
        """Primeiro retorno diário deve ser NaN (sem dia anterior)."""
        from ibovespa_analysis import fetch_ibovespa_history

        df = fetch_ibovespa_history()
        assert pd.isna(df["Daily_Return"].iloc[0]), "Primeiro Daily_Return deve ser NaN"


# ---------------------------------------------------------------------------
# 2. Projeção ARIMA
# ---------------------------------------------------------------------------


class TestProjectIbovespa:
    """Testa a função project_ibovespa."""

    @pytest.fixture(scope="class")
    def historical_df(self):
        from ibovespa_analysis import fetch_ibovespa_history

        return fetch_ibovespa_history()

    def test_retorna_dataframe(self, historical_df):
        from ibovespa_analysis import project_ibovespa

        df = project_ibovespa(historical_df)
        assert isinstance(df, pd.DataFrame), "Deve retornar um DataFrame"

    def test_colunas_obrigatorias(self, historical_df):
        from ibovespa_analysis import project_ibovespa

        df = project_ibovespa(historical_df)
        expected = {"Date", "Projected_Close", "CI_Lower_95", "CI_Upper_95"}
        assert expected.issubset(set(df.columns)), (
            f"Colunas ausentes: {expected - set(df.columns)}"
        )

    def test_projecao_nao_vazia(self, historical_df):
        from ibovespa_analysis import project_ibovespa

        df = project_ibovespa(historical_df)
        assert len(df) > 0, "Projeção não pode ser vazia"

    def test_projecao_aproximadamente_2_anos(self, historical_df):
        from ibovespa_analysis import project_ibovespa

        df = project_ibovespa(historical_df)
        # 2 anos úteis ≈ 504 dias; tolerância de ±20%
        assert 400 <= len(df) <= 620, (
            f"Projeção deve cobrir ~2 anos úteis, mas tem {len(df)} pontos"
        )

    def test_ci_lower_menor_que_projected(self, historical_df):
        from ibovespa_analysis import project_ibovespa

        df = project_ibovespa(historical_df)
        assert (df["CI_Lower_95"] <= df["Projected_Close"]).all(), (
            "CI_Lower_95 deve ser ≤ Projected_Close"
        )

    def test_ci_upper_maior_que_projected(self, historical_df):
        from ibovespa_analysis import project_ibovespa

        df = project_ibovespa(historical_df)
        assert (df["CI_Upper_95"] >= df["Projected_Close"]).all(), (
            "CI_Upper_95 deve ser ≥ Projected_Close"
        )

    def test_datas_futuras(self, historical_df):
        from ibovespa_analysis import project_ibovespa

        df = project_ibovespa(historical_df)
        last_historical = pd.to_datetime(historical_df["Date"]).max()
        first_projected = pd.to_datetime(df["Date"]).min()
        assert first_projected > last_historical, (
            "Projeção deve iniciar após o último dado histórico"
        )

    def test_projected_close_positivo(self, historical_df):
        from ibovespa_analysis import project_ibovespa

        df = project_ibovespa(historical_df)
        assert (df["Projected_Close"] > 0).all(), "Projected_Close deve ser positivo"


# ---------------------------------------------------------------------------
# 3. Busca de ativos da carteira
# ---------------------------------------------------------------------------


class TestFetchPortfolioAssets:
    """Testa a função fetch_portfolio_assets."""

    @pytest.fixture(scope="class")
    def assets(self):
        from ibovespa_analysis import fetch_portfolio_assets

        return fetch_portfolio_assets()

    def test_retorna_dicionario(self, assets):
        assert isinstance(assets, dict), "Deve retornar um dicionário"

    def test_chaves_obrigatorias(self, assets):
        expected_keys = {"rf_lp_high", "lft_2031", "lca_bb_prefixada"}
        assert expected_keys.issubset(set(assets.keys())), (
            f"Chaves ausentes: {expected_keys - set(assets.keys())}"
        )

    def test_cada_ativo_tem_dataframe(self, assets):
        for key, val in assets.items():
            assert isinstance(val["data"], pd.DataFrame), (
                f"Ativo '{key}' deve ter DataFrame em 'data'"
            )

    def test_cada_ativo_tem_metadados(self, assets):
        for key, val in assets.items():
            assert "source" in val, f"Ativo '{key}' deve ter 'source'"
            assert "period" in val, f"Ativo '{key}' deve ter 'period'"
            assert "proxy_used" in val, f"Ativo '{key}' deve ter 'proxy_used'"

    def test_cada_ativo_tem_coluna_value(self, assets):
        for key, val in assets.items():
            df = val["data"]
            assert "Value" in df.columns, f"Ativo '{key}' deve ter coluna 'Value'"
            assert "Date" in df.columns, f"Ativo '{key}' deve ter coluna 'Date'"

    def test_valores_positivos(self, assets):
        for key, val in assets.items():
            df = val["data"]
            validos = df["Value"].dropna()
            if len(validos) > 0:
                assert (validos > 0).all(), (
                    f"Ativo '{key}': valores negativos ou zero inválidos"
                )

    def test_dataframe_nao_vazio(self, assets):
        for key, val in assets.items():
            df = val["data"]
            assert len(df) > 0, f"Ativo '{key}' retornou DataFrame vazio"

    def test_source_nao_vazio(self, assets):
        for key, val in assets.items():
            assert val["source"] and len(val["source"]) > 0, (
                f"Ativo '{key}' deve ter source preenchido"
            )


# ---------------------------------------------------------------------------
# 4. Normalização para comparação
# ---------------------------------------------------------------------------


class TestNormalizeSeries:
    """Testa a função normalize_series."""

    def test_base_100_na_data_base(self):
        from ibovespa_analysis import normalize_series

        dates = pd.date_range("2020-01-02", periods=5, freq="B")
        values = pd.Series([100.0, 110.0, 105.0, 120.0, 115.0])
        df = pd.DataFrame({"Date": dates, "Value": values})
        result = normalize_series(df, "Value")
        # Primeiro valor deve ser 100
        assert abs(result["Normalized"].iloc[0] - 100.0) < 1e-9, (
            "Primeiro valor normalizado deve ser 100"
        )

    def test_proporcao_mantida(self):
        from ibovespa_analysis import normalize_series

        dates = pd.date_range("2020-01-02", periods=3, freq="B")
        values = pd.Series([200.0, 400.0, 300.0])
        df = pd.DataFrame({"Date": dates, "Value": values})
        result = normalize_series(df, "Value")
        assert abs(result["Normalized"].iloc[1] - 200.0) < 1e-9, (
            "200→400 normalizado de 100 = 200"
        )
        assert abs(result["Normalized"].iloc[2] - 150.0) < 1e-9, (
            "200→300 normalizado de 100 = 150"
        )

    def test_retorna_dataframe_com_coluna(self):
        from ibovespa_analysis import normalize_series

        dates = pd.date_range("2020-01-02", periods=3, freq="B")
        df = pd.DataFrame({"Date": dates, "Value": [50.0, 55.0, 52.0]})
        result = normalize_series(df, "Value")
        assert "Normalized" in result.columns
        assert "Date" in result.columns

    def test_raises_se_valor_base_zero(self):
        from ibovespa_analysis import normalize_series

        dates = pd.date_range("2020-01-02", periods=3, freq="B")
        df = pd.DataFrame({"Date": dates, "Value": [0.0, 10.0, 20.0]})
        with pytest.raises(ValueError):
            normalize_series(df, "Value")


# ---------------------------------------------------------------------------
# 5. Geração do gráfico
# ---------------------------------------------------------------------------


class TestGenerateChart:
    """Testa a função generate_comparison_chart."""

    @pytest.fixture(scope="class")
    def all_data(self):
        from ibovespa_analysis import (
            fetch_ibovespa_history,
            fetch_portfolio_assets,
            project_ibovespa,
        )

        ibov = fetch_ibovespa_history()
        proj = project_ibovespa(ibov)
        assets = fetch_portfolio_assets()
        return ibov, proj, assets

    def test_arquivo_png_criado(self, all_data, tmp_path):
        from ibovespa_analysis import generate_comparison_chart

        ibov, proj, assets = all_data
        output_path = tmp_path / "test_chart.png"
        generate_comparison_chart(ibov, proj, assets, output_path=str(output_path))
        assert output_path.exists(), "Arquivo PNG deve ser criado"
        assert output_path.stat().st_size > 0, "Arquivo PNG não pode ser vazio"

    def test_cria_diretorio_outputs_se_nao_existir(self, all_data, tmp_path):
        from ibovespa_analysis import generate_comparison_chart

        ibov, proj, assets = all_data
        subdir = tmp_path / "subdir_novo" / "outputs"
        output_path = subdir / "chart.png"
        generate_comparison_chart(ibov, proj, assets, output_path=str(output_path))
        assert output_path.exists(), "Deve criar diretórios automaticamente"


# ---------------------------------------------------------------------------
# 6. Acumulação de taxas em índice (_accumulate_rate_to_index)
# ---------------------------------------------------------------------------


class TestAccumulateRateToIndex:
    """
    Valida _accumulate_rate_to_index contra invariantes matemáticos.

    BCB série 12 (CDI) retorna taxa % ao dia, ex: 0.047 = 0.047%/dia.
    Fator diário: 1 + 0.047/100 = 1.00047.
    Em 252 dias úteis: 1.00047^252 ≈ 1.126 → índice de 100 vai a ~112.6.
    """

    def _make_constant_rate_df(
        self, rate_pct_per_day: float, n_days: int
    ) -> pd.DataFrame:
        """DataFrame sintético com taxa diária constante."""
        dates = pd.bdate_range("2024-01-02", periods=n_days)
        return pd.DataFrame({"Date": dates, "Rate": [rate_pct_per_day] * n_days})

    def test_indice_inicia_em_100(self):
        """O primeiro valor do índice deve ser exatamente start_value=100."""
        from ibovespa_analysis import _accumulate_rate_to_index

        df = self._make_constant_rate_df(0.047, 252)
        result = _accumulate_rate_to_index(df)
        assert abs(result["Value"].iloc[0] - 100.0) < 1e-6, (
            f"Índice deve iniciar em 100.0, mas foi {result['Value'].iloc[0]:.6f}"
        )

    def test_cdi_252_dias_uteis_aproximadamente_113(self):
        """
        252 dias úteis com 0.047%/dia deve resultar em ~112-114.

        1.00047^252 ≈ 1.1257 → índice final ≈ 112.57.
        Tolerância ±5 para absorver variações de hora e calendário.
        Se este teste falhar com valor >1000, o bug de overflow voltou.
        """
        from ibovespa_analysis import _accumulate_rate_to_index

        df = self._make_constant_rate_df(0.047, 252)
        result = _accumulate_rate_to_index(df)
        final_value = result["Value"].iloc[-1]
        assert 108.0 <= final_value <= 118.0, (
            f"CDI 0.047%/dia × 252 dias deve resultar em ~112-113, "
            f"mas foi {final_value:.4f}. "
            f"Valores > 200 indicam overflow (bug de double-scaling)."
        )

    def test_sem_overflow(self):
        """
        Garante que não há overflow (bug anterior causava valores ~10000+).
        Com qualquer taxa CDI realista, o índice em 5 anos não passa de 200.
        """
        from ibovespa_analysis import _accumulate_rate_to_index

        df = self._make_constant_rate_df(0.047, 5 * 252)
        result = _accumulate_rate_to_index(df)
        assert result["Value"].max() < 250.0, (
            f"Overflow detectado: valor máximo = {result['Value'].max():.2f}. "
            f"Esperado < 250 para 5 anos de CDI real."
        )

    def test_crescimento_monotono_com_taxa_positiva(self):
        """Com taxa positiva constante, o índice deve crescer monotonicamente."""
        from ibovespa_analysis import _accumulate_rate_to_index

        df = self._make_constant_rate_df(0.047, 10)
        result = _accumulate_rate_to_index(df)
        assert result["Value"].is_monotonic_increasing, (
            "Com taxa diária positiva, índice deve crescer a cada dia"
        )

    def test_retorna_dataframe_com_colunas_date_e_value(self):
        """Formato de saída: DataFrame com colunas Date e Value."""
        from ibovespa_analysis import _accumulate_rate_to_index

        df = self._make_constant_rate_df(0.047, 5)
        result = _accumulate_rate_to_index(df)
        assert "Date" in result.columns, "Coluna 'Date' ausente"
        assert "Value" in result.columns, "Coluna 'Value' ausente"
        assert len(result) == 5, f"Esperado 5 linhas, obtido {len(result)}"

    def test_start_value_customizado(self):
        """start_value diferente de 100 deve ser respeitado."""
        from ibovespa_analysis import _accumulate_rate_to_index

        df = self._make_constant_rate_df(0.047, 10)
        result = _accumulate_rate_to_index(df, start_value=1000.0)
        assert abs(result["Value"].iloc[0] - 1000.0) < 1e-4, (
            f"Índice deve iniciar em 1000.0, mas foi {result['Value'].iloc[0]:.4f}"
        )


# ---------------------------------------------------------------------------
# 7. Testes para o bug série 432 — rate_type (TDD antes da correção)
# ---------------------------------------------------------------------------


def test_accumulate_daily_rate_cdi():
    """CDI: 0.047% ao dia por 252 dias deve resultar em ~113 (≈13% ao ano)."""
    from ibovespa_analysis import _accumulate_rate_to_index

    dates = pd.date_range("2024-01-01", periods=252, freq="B")
    rate_df = pd.DataFrame({"Date": dates, "Rate": 0.047})
    result = _accumulate_rate_to_index(rate_df, rate_type="daily_pct")
    final = result["Value"].iloc[-1]
    assert 110 <= final <= 116, f"CDI acumulado esperado ~113, obtido {final:.2f}"


def test_accumulate_annual_rate_selic():
    """SELIC: 13.75% ao ano por 252 dias deve resultar em ~113.75."""
    from ibovespa_analysis import _accumulate_rate_to_index

    dates = pd.date_range("2024-01-01", periods=252, freq="B")
    rate_df = pd.DataFrame({"Date": dates, "Rate": 13.75})
    result = _accumulate_rate_to_index(rate_df, rate_type="annual_pct")
    final = result["Value"].iloc[-1]
    assert 110 <= final <= 117, f"SELIC acumulado esperado ~113.75, obtido {final:.2f}"


def test_accumulate_wrong_type_raises():
    """rate_type inválido deve levantar ValueError."""
    from ibovespa_analysis import _accumulate_rate_to_index

    dates = pd.date_range("2024-01-01", periods=5, freq="B")
    rate_df = pd.DataFrame({"Date": dates, "Rate": 0.047})
    with pytest.raises(ValueError):
        _accumulate_rate_to_index(rate_df, rate_type="invalid")
