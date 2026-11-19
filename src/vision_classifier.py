
import os
import json
from io import BytesIO

from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image, UnidentifiedImageError

load_dotenv()

CATEGORIAS = {
    "ALAGAMENTO",
    "BUEIRO_OBSTRUIDO",
    "ARVORE_CAIDA",
    "SEM_INCIDENTE",
    "OUTRO"
}

GRAVIDADES = {
    "BAIXA", "MEDIA", "ALTA", "INDETERMINADA"
}


def analisar_imagem(conteudo: bytes):
    # 1. Validar a imagem
    try:
        with Image.open(BytesIO(conteudo)) as imagem:
            imagem.verify()

        with Image.open(BytesIO(conteudo)) as imagem:
            formato = imagem.format

        if formato not in ("JPEG", "PNG", "WEBP"):
            raise ValueError("Formato não permitido.")

    except (UnidentifiedImageError, OSError, ValueError):
        return {
            "imagem_valida": False,
            "modo": "VALIDACAO",
            "mensagem": "Arquivo de imagem inválido."
        }

    # 2. Verificar a chave
    chave = os.getenv("GEMINI_API_KEY")

    if not chave:
        return resposta_indisponivel(
            "Chave do Gemini não configurada."
        )

    # 3. Preparar a análise
    mime_types = {
        "JPEG": "image/jpeg",
        "PNG": "image/png",
        "WEBP": "image/webp"
    }

    prompt = """
    Você é o sistema AlertaCom-IA.

    Analise a fotografia e identifique possíveis
    incidentes urbanos.

    Categorias permitidas:
    ALAGAMENTO, BUEIRO_OBSTRUIDO,
    ARVORE_CAIDA, SEM_INCIDENTE, OUTRO.

    Gravidades permitidas:
    BAIXA, MEDIA, ALTA, INDETERMINADA.

    Retorne um JSON contendo:
    categoria, gravidade e descricao.

    Descreva somente o que for visível.
    Não invente informações.
    Não afirme que uma área é segura
    apenas com base na fotografia.
    """

    # 4. Tentar usar a IA real
    try:
        cliente = genai.Client(
            api_key=chave,
            http_options=types.HttpOptions(
                timeout=15000
            )
        )

        resposta = cliente.models.generate_content(
            model="gemini-3.8-flash",
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=conteudo,
                    mime_type=mime_types[formato]
                )
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                max_output_tokens=300
            )
        )

        if not resposta.text:
            raise ValueError("Resposta vazia do Gemini.")

        resultado = json.loads(resposta.text)

        categoria = resultado.get("categoria", "OUTRO")
        gravidade = resultado.get(
            "gravidade", "INDETERMINADA"
        )

        if categoria not in CATEGORIAS:
            categoria = "OUTRO"

        if gravidade not in GRAVIDADES:
            gravidade = "INDETERMINADA"

        return {
            "imagem_valida": True,
            "modo": "IA_REAL",
            "categoria": categoria,
            "gravidade": gravidade,
            "descricao": resultado.get("descricao", "")
        }

    except Exception as erro:
        print(
            f"Falha na IA: {type(erro).__name__}: {erro}",
            flush=True
        )

        return resposta_indisponivel(
            "O Gemini não conseguiu concluir a análise."
        )


def resposta_indisponivel(mensagem):
    return {
        "imagem_valida": True,
        "modo": "DEMONSTRACAO",
        "categoria": "NAO_ANALISADO",
        "gravidade": "INDETERMINADA",
        "descricao": (
            "A imagem foi recebida e validada, "
            "mas não foi analisada pela IA."
        ),
        "mensagem": mensagem
    }
