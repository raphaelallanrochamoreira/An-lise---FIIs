import pandas as pd
import os
import chardet

RAW_DIR = "data/raw"

def detectar_encoding(caminho):
    with open(caminho, "rb") as f:
        resultado = chardet.detect(f.read(100000))
    return resultado["encoding"]

def limpar_csv(caminho):
    enc = detectar_encoding(caminho)
    df = pd.read_csv(caminho, sep=";", encoding=enc, low_memory=False)

    # Remove colunas 100% vazias
    df.dropna(axis=1, how="all", inplace=True)

    # Padroniza nomes de colunas
    df.columns = (
        df.columns
        .str.strip()
        .str.upper()
        .str.replace(" ", "_")
        .str.replace("/", "_")
    )

    # Converte datas
    for col in df.columns:
        if "DT_" in col or "DATA" in col:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Converte valores numéricos
    for col in df.columns:
        if df[col].dtype == object:
            tentativa = df[col].str.replace(",", ".", regex=False)
            df[col] = pd.to_numeric(tentativa, errors="ignore")

    return df

def processar_todos():
    frames = []
    for pasta_ano in os.listdir(RAW_DIR):
        caminho_pasta = os.path.join(RAW_DIR, pasta_ano)
        if not os.path.isdir(caminho_pasta):
            continue
        for arquivo in os.listdir(caminho_pasta):
            if arquivo.endswith(".csv"):
                caminho_csv = os.path.join(caminho_pasta, arquivo)
                print(f"Limpando: {arquivo}")
                df = limpar_csv(caminho_csv)
                frames.append(df)
    return frames

if __name__ == "__main__":
    frames = processar_todos()
    print(f"\n{len(frames)} arquivo(s) processado(s).")
    if frames:
        print(f"Colunas do primeiro arquivo: {list(frames[0].columns)}")
