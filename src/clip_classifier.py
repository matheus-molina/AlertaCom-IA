
from functools import lru_cache
from io import BytesIO

import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor


MODELO = "openai/clip-vit-base-patch32"

CATEGORIAS = {
    "ALAGAMENTO": "A street flooded with water and submerged cars",
    "BUEIRO_OBSTRUIDO": "A clogged storm drain full of trash",
    "ARVORE_CAIDA": "A fallen tree blocking a city street",
    "BURACO_NA_VIA": "A large pothole in a damaged asphalt road filled with muddy water",
    "SEM_INCIDENTE": "A normal city street with no visible incident",
}


@lru_cache(maxsize=1)
def carregar_modelo():
    processador = CLIPProcessor.from_pretrained(MODELO)
    modelo = CLIPModel.from_pretrained(MODELO)
    modelo.eval()
    return processador, modelo


def classificar_imagem(conteudo: bytes):
    imagem = Image.open(BytesIO(conteudo)).convert("RGB")

    processador, modelo = carregar_modelo()

    entradas = processador(
        text=list(CATEGORIAS.values()),
        images=imagem,
        return_tensors="pt",
        padding=True
    )

    with torch.no_grad():
        saida = modelo(**entradas)
        pontuacoes = saida.logits_per_image.softmax(dim=1)[0]

    indice = int(pontuacoes.argmax().item())
    categoria = list(CATEGORIAS.keys())[indice]

    return {
        "categoria": categoria,
        "pontuacao_relativa": round(
            float(pontuacoes[indice].item()), 4
        ),
        "modelo": MODELO
    }
