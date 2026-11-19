
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

chave = os.getenv("GEMINI_API_KEY")

if not chave:
    print("ERRO: Chave do Gemini não encontrada!")
    raise SystemExit(1)

print("Conectando ao Gemini...", flush=True)

try:
    cliente = genai.Client(
        api_key=chave,
        http_options=types.HttpOptions(timeout=15000)
    )

    resposta = cliente.models.generate_content(
        model="gemini-3.7-flash",
        contents="Responda apenas: AlertaCom funcionando!"
    )

    print("Resposta do Gemini:")
    print(resposta.text)

except Exception as erro:
    print(f"Erro: {type(erro).__name__}")
    print(str(erro))
