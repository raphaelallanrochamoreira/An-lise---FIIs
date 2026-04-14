import pandas as pd
import os
import chardet

RAW_DIR = "data/raw"
OUTPUT = "data/processed/fii_consolidado.csv"

def detectar_encoding(caminho):
    with open(caminho, "rb") as f:
        resultado = chardet.detect(f.read(100000))
    return resultado["encoding"]

def carregar_csv(caminho):
    enc = detectar_encoding(caminho)
    df = pd.read_csv(caminho, sep=";", encoding=enc, low_memory=False)
    df.dropna(axis=1, how="all", inplace=True)
    df.columns = (
        df.columns
        .str.strip()
        .str.upper()
        .str.replace(" ", "_")
        .str.replace("/", "_")
    )
    return df

def consolidar():
    frames = []
    for pasta_ano in sorted(os.listdir(RAW_DIR)):
        caminho_pasta = os.path.join(RAW_DIR, pasta_ano)
        if not os.path.isdir(caminho_pasta):
            continue
        for arquivo in sorted(os.listdir(caminho_pasta)):
            if arquivo.endswith(".csv"):
                caminho_csv = os.path.join(caminho_pasta, arquivo)
                print(f"Carregando: {arquivo}")
                df = carregar_csv(caminho_csv)
                frames.append(df)

    if not frames:
        print("Nenhum CSV encontrado em data/raw/. Rode primeiro o 01_extrair.py.")
        return

    consolidado = pd.concat(frames, ignore_index=True)
    os.makedirs("data/processed", exist_ok=True)
    consolidado.to_csv(OUTPUT, index=False, sep=";", encoding="utf-8-sig")
    print(f"\nConsolidado salvo em: {OUTPUT}")
    print(f"Total de linhas: {len(consolidado):,}")
    print(f"Total de colunas: {len(consolidado.columns)}")
    print(f"Colunas: {list(consolidado.columns)}")

if __name__ == "__main__":
    consolidar()
