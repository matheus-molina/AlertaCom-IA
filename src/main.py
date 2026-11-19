
from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image, UnidentifiedImageError
from io import BytesIO

from src.clip_classifier import classificar_imagem

app = FastAPI(
    title="AlertaCom - Inteligência Artificial",
    description="API para análise de incidentes urbanos e orientações de segurança.",
    version="1.0.0"
)


@app.get("/")
def inicio():
    return {
        "projeto": "AlertaCom",
        "modulo": "Inteligência Artificial",
        "status": "API funcionando!"
    }


@app.get("/health")
def verificar_saude():
    return {
        "status": "online"
    }


@app.post("/analyze-incident")
async def analisar_incidente(arquivo: UploadFile = File(...)):

    if not arquivo.content_type or not arquivo.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Envie um arquivo de imagem."
        )

    conteudo = await arquivo.read()

    if len(conteudo) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="A imagem deve ter no máximo 5 MB."
        )

    try:
        imagem = Image.open(BytesIO(conteudo))
        imagem.verify()
    except (UnidentifiedImageError, OSError, ValueError):
        raise HTTPException(
            status_code=400,
            detail="Imagem inválida ou corrompida."
        )

    try:
        resultado = classificar_imagem(conteudo)
    except Exception as erro:
        print(f"Erro ao classificar imagem: {erro}")
        raise HTTPException(
            status_code=503,
            detail="Não foi possível concluir a análise."
        )

    return {
        "imagem_valida": True,
        "modo": "CLIP_LOCAL",
        "categoria": resultado["categoria"],
        "pontuacao_relativa": resultado["pontuacao_relativa"],
        "modelo": resultado["modelo"]
    }
