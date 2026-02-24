"""
Script para identificar o CNPJ do fundo RF LP High do Banco do Brasil.

Estratégia: filtrar pelo CNPJ do gestor BB DTVM (30.822.936/0001-69) e/ou
pelo nome do gestor/administrador contendo BB/BRASIL, depois listar todos os
fundos em funcionamento do tipo Renda Fixa LP para identificar qual corresponde
ao nome comercial "RF LP High" exibido na plataforma do BB.
"""

import io

import pandas as pd
import requests

BB_DTVM_CNPJ = "30.822.936/0001-69"  # CNPJ oficial da BB DTVM S.A.

print("Baixando cadastro CVM (cad_fi.csv)...")
r = requests.get(
    "https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv",
    timeout=60,
)
df = pd.read_csv(
    io.StringIO(r.content.decode("latin-1")),
    sep=";",
    dtype=str,
    low_memory=False,
)
print(f"Total de fundos no cadastro: {len(df)}")
print(f"Colunas disponíveis: {list(df.columns)}\n")

# Apenas fundos em funcionamento
ativos = df[df["SIT"].str.upper().str.contains("FUNCIONAMENTO", na=False)].copy()
print(f"Fundos em funcionamento: {len(ativos)}")

# --- Busca 1: pelo CNPJ da BB DTVM no campo CNPJ_GESTOR ---
if "CNPJ_GESTOR" in df.columns:
    mask_cnpj = ativos["CNPJ_GESTOR"].str.strip() == BB_DTVM_CNPJ
    bbdtvm = ativos[mask_cnpj].copy()
    print(
        f"\n=== Gestor CNPJ={BB_DTVM_CNPJ} (BB DTVM) — EM FUNCIONAMENTO ({len(bbdtvm)}) ==="
    )
    # Filtrar por LP no nome
    lp_funds = bbdtvm[bbdtvm["DENOM_SOCIAL"].str.upper().str.contains(" LP", na=False)]
    print(f"  └─ Contendo ' LP' no nome: {len(lp_funds)}")
    for _, row in pd.DataFrame(lp_funds).sort_values("DENOM_SOCIAL").iterrows():
        print(f"    {row['CNPJ_FUNDO']}  |  {row['DENOM_SOCIAL']}")
    if len(lp_funds) == 0:
        print("  ── Nenhum LP encontrado; listando todos os fundos BB DTVM RF ativas:")
        rf_funds = bbdtvm[
            bbdtvm["DENOM_SOCIAL"]
            .str.upper()
            .str.contains("RENDA FIXA|RF", na=False, regex=True)
        ]
        for _, row in pd.DataFrame(rf_funds).sort_values("DENOM_SOCIAL").head(50).iterrows():
            print(f"    {row['CNPJ_FUNDO']}  |  {row['DENOM_SOCIAL']}")

# --- Busca 2: pelo nome do gestor contendo BB DTVM ---
col_gestor_nome = next(
    (c for c in df.columns if "GESTOR" in c.upper() and "CNPJ" not in c.upper()), None
)
if col_gestor_nome:
    mask_nome = (
        ativos[col_gestor_nome]
        .str.upper()
        .str.contains("BB DTVM", na=False, regex=False)
    )
    por_nome = ativos[mask_nome]
    print(
        f"\n=== {col_gestor_nome} contém 'BB DTVM' — EM FUNCIONAMENTO ({len(por_nome)}) ==="
    )
    lp_por_nome = por_nome[
        por_nome["DENOM_SOCIAL"].str.upper().str.contains(" LP", na=False)
    ]
    print(f"  └─ Contendo ' LP' no nome: {len(lp_por_nome)}")
    for _, row in pd.DataFrame(lp_por_nome).sort_values("DENOM_SOCIAL").iterrows():
        print(
            f"    {row['CNPJ_FUNDO']}  |  {row['DENOM_SOCIAL']}  |  {row.get(col_gestor_nome, '')}"
        )

# --- Busca 3: administrador contendo BB ou BANCO DO BRASIL ---
col_adm = next(
    (c for c in df.columns if "ADM" in c.upper() and "CNPJ" not in c.upper()), None
)
if col_adm:
    mask_adm = ativos[col_adm].str.upper().str.contains(
        "BB DTVM|BANCO DO BRASIL|BB S.A", na=False, regex=True
    ) & ativos["DENOM_SOCIAL"].str.upper().str.contains(" LP", na=False)
    por_adm = ativos[mask_adm]
    print(
        f"\n=== {col_adm} contém BB/BRASIL + nome contém ' LP' — EM FUNCIONAMENTO ({len(por_adm)}) ==="
    )
    for _, row in pd.DataFrame(por_adm).sort_values("DENOM_SOCIAL").iterrows():
        print(
            f"    {row['CNPJ_FUNDO']}  |  {row['DENOM_SOCIAL']}  |  {row.get(col_adm, '')}"
        )

# --- Busca 4: nome começa com "BB RF" ou "BB RENDA FIXA" em qualquer status ---
mask_bbrf = (
    df["DENOM_SOCIAL"]
    .str.upper()
    .str.contains(r"^BB RF|^BB RENDA FIXA", na=False, regex=True)
)
bbrf_all = df[mask_bbrf]
lp_all = bbrf_all[bbrf_all["DENOM_SOCIAL"].str.upper().str.contains(" LP", na=False)]
print(
    f"\n=== Nome começa com 'BB RF'/'BB RENDA FIXA' E contém ' LP' — TODOS STATUS ({len(lp_all)}) ==="
)
for _, row in pd.DataFrame(lp_all).sort_values(["SIT", "DENOM_SOCIAL"]).iterrows():
    print(f"  {row['CNPJ_FUNDO']}  |  {row['DENOM_SOCIAL']}  |  {row['SIT']}")

# --- Busca 5: FIC — fundo em cotas de BB LP ---
mask_fic = (
    ativos["DENOM_SOCIAL"].str.upper().str.contains("BB", na=False)
    & ativos["DENOM_SOCIAL"].str.upper().str.contains(" LP", na=False)
    & ativos["DENOM_SOCIAL"].str.upper().str.contains("FIC|COTAS", na=False, regex=True)
)
fic_bb = ativos[mask_fic]
print(f"\n=== FIC/Cotas BB LP — EM FUNCIONAMENTO ({len(fic_bb)}) ===")
for _, row in pd.DataFrame(fic_bb).sort_values("DENOM_SOCIAL").iterrows():
    print(f"  {row['CNPJ_FUNDO']}  |  {row['DENOM_SOCIAL']}")

print("\nConcluído.")
