"""
processar_vendas.py
-------------------
Lê os dados brutos de vendas (dados/vendas_brutas.csv), limpa e organiza
tudo automaticamente, e salva um arquivo pronto para o Power BI
(dados/vendas_tratadas.csv).

Ideia do projeto: em vez de arrumar a planilha na mão toda semana,
este script faz a limpeza sozinho em segundos.
"""

from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
ARQUIVO_ENTRADA = BASE_DIR / "dados" / "vendas_brutas.csv"
ARQUIVO_SAIDA = BASE_DIR / "dados" / "vendas_tratadas.csv"

# Catálogo oficial de modelos: garante o nome certo mesmo pra casos que
# title() erraria (ex.: "GT-R" viraria "Gt-R", "e-POWER" viraria "E-Power")
MODELOS_VALIDOS = {
    "kicks": "Kicks",
    "sentra": "Sentra",
    "versa": "Versa",
    "frontier": "Frontier",
    "march": "March",
    "leaf": "Leaf",
}


def padronizar_modelo(valor):
    """Usa o nome oficial do catálogo; se o modelo não está na lista, cai pra title()."""
    if pd.isna(valor):
        return valor
    chave = valor.strip().lower()
    return MODELOS_VALIDOS.get(chave, valor.strip().title())


def carregar(caminho):
    """Lê o CSV bruto e devolve uma tabela (DataFrame)."""
    print(f"Lendo {caminho} ...")
    return pd.read_csv(caminho, dtype=str)  # lê tudo como texto para tratar sem surpresas


def limpar_texto(df):
    """Tira espaços sobrando e padroniza maiúsculas/minúsculas."""
    # Remove espaços no começo e no fim de todas as colunas de texto
    for coluna in ["modelo", "concessionaria", "regiao", "vendedor"]:
        df[coluna] = df[coluna].str.strip()

    # Padroniza o nome do modelo pelo catálogo oficial: "kicks", "KICKS", " Kicks " -> "Kicks"
    df["modelo"] = df["modelo"].apply(padronizar_modelo)

    # Padroniza a concessionária: "nissan zona sul" -> "Nissan Zona Sul"
    df["concessionaria"] = df["concessionaria"].str.title()

    return df


def converter_preco(valor):
    """
    Converte o preço para número.
    Aceita tanto "132167.35" quanto "R$ 201.902,15" (padrão brasileiro).
    """
    if pd.isna(valor):
        return None
    texto = str(valor).replace("R$", "").strip()
    if texto == "":
        return None
    # Se tem vírgula, está no formato BR (ponto = milhar, vírgula = decimal)
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    return float(texto)


def tratar_numeros(df):
    """Converte preço e unidades para número de verdade e cria a coluna de receita."""
    df["preco_unitario"] = df["preco_unitario"].apply(converter_preco)
    # 'unidades' pode vir vazia; converte para número (vazio vira NaN)
    df["unidades"] = pd.to_numeric(df["unidades"], errors="coerce")

    # Receita = quantas unidades x preço de cada uma
    df["receita"] = df["unidades"] * df["preco_unitario"]
    return df


def tratar_datas(df):
    """Converte a coluna de data (que vem em vários formatos) para data de verdade."""
    df["data"] = pd.to_datetime(df["data"], format="mixed", dayfirst=True, errors="coerce")
    # Cria colunas extras que ajudam muito no Power BI
    df["ano"] = df["data"].dt.year
    df["mes"] = df["data"].dt.month
    return df


def remover_problemas(df):
    """Remove linhas duplicadas (mesmo id_venda) e linhas sem informação essencial."""
    antes = len(df)
    # Duplicata de verdade = mesmo id_venda, não "linha inteira igual" (duas vendas
    # distintas podem coincidir em todos os outros campos por acaso)
    df = df.drop_duplicates(subset=["id_venda"])
    duplicadas = antes - len(df)

    # Descarta linhas sem data, sem unidades ou sem preço (não dá pra usar)
    antes_incompletas = len(df)
    df = df.dropna(subset=["data", "unidades", "preco_unitario"])
    incompletas = antes_incompletas - len(df)

    # Região em branco não invalida a venda, só marca como não informada
    df["regiao"] = df["regiao"].fillna("Não informado")

    # Depois do dropna não sobra NaN em 'unidades', então dá pra virar inteiro
    # de verdade (sem o ".0" que o Power BI mostraria como decimal)
    df["unidades"] = df["unidades"].astype(int)

    print(f"Removidas {duplicadas} linhas duplicadas e {incompletas} linhas incompletas.")
    return df


def resumo(df):
    """Mostra um resumão no terminal só pra conferir se deu certo."""
    print("\n===== RESUMO =====")
    print(f"Linhas finais: {len(df)}")
    print(f"Receita total: R$ {df['receita'].sum():,.2f}")
    print("\nReceita por modelo:")
    print(df.groupby("modelo")["receita"].sum().sort_values(ascending=False).round(2))
    print("==================\n")


def main():
    df = carregar(ARQUIVO_ENTRADA)
    df = limpar_texto(df)
    df = tratar_numeros(df)
    df = tratar_datas(df)
    df = remover_problemas(df)

    # Reordena as colunas para ficar organizado
    df = df[["id_venda", "data", "ano", "mes", "modelo", "concessionaria", "regiao",
             "vendedor", "unidades", "preco_unitario", "receita"]]

    df.to_csv(ARQUIVO_SAIDA, index=False, encoding="utf-8-sig")
    print(f"Arquivo pronto para o Power BI salvo em: {ARQUIVO_SAIDA}")
    resumo(df)


if __name__ == "__main__":
    main()
