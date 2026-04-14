import zipfile
import os

RAW_DIR = "data/raw"
META_DIR = "data/meta"

def extrair_zips(pasta):
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".zip"):
            caminho_zip = os.path.join(pasta, arquivo)
            destino = os.path.join(pasta, arquivo.replace(".zip", ""))
            os.makedirs(destino, exist_ok=True)
            with zipfile.ZipFile(caminho_zip, "r") as z:
                z.extractall(destino)
            print(f"Extraído: {arquivo} → {destino}/")

if __name__ == "__main__":
    extrair_zips(RAW_DIR)
    extrair_zips(META_DIR)
    print("Extração concluída.")
