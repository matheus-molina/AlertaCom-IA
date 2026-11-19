
from pathlib import Path
from src.clip_classifier import classificar_imagem

caminho = Path("testes/alagamento.jpeg")

with open(caminho, "rb") as arquivo:
    conteudo = arquivo.read()

print("Analisando imagem com CLIP...")

resultado = classificar_imagem(conteudo)

print("\nResultado da análise:")
print(f"Categoria: {resultado['categoria']}")
print(f"Pontuação relativa: {resultado['pontuacao_relativa']:.2%}")
print(f"Modelo: {resultado['modelo']}")
