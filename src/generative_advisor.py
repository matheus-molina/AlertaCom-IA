
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODELO = "google/flan-t5-small"

tokenizer = None
modelo = None

SITUACOES = {
    "ALAGAMENTO": "A street is flooded.",
    "ARVORE_CAIDA": "A tree has fallen across the road.",
    "BUEIRO_OBSTRUIDO": "A storm drain is blocked.",
    "BURACO_NA_VIA": "There is a large pothole in the road.",
    "SEM_INCIDENTE": "The street appears normal."
}

ORIENTACOES_SEGURAS = {
    "ALAGAMENTO": "Não atravesse áreas alagadas. Procure uma rota segura.",
    "ARVORE_CAIDA": "Mantenha distância da árvore caída e evite a área.",
    "BUEIRO_OBSTRUIDO": "Evite a área obstruída e comunique o problema ao órgão responsável.",
    "BURACO_NA_VIA": "Evite passar pelo buraco e sinalize o risco às autoridades responsáveis.",
    "SEM_INCIDENTE": "Nenhum incidente evidente foi identificado na imagem."
}


def carregar_modelo():
    global tokenizer, modelo

    if tokenizer is None or modelo is None:
        print("Carregando FLAN-T5...")

        tokenizer = AutoTokenizer.from_pretrained(MODELO)

        modelo = AutoModelForSeq2SeqLM.from_pretrained(
            MODELO,
            dtype=torch.float32
        )

        modelo.eval()


def gerar_orientacao(categoria):
    if categoria not in SITUACOES:
        return {
            "orientacao_gerada": "",
            "orientacao_segura": "Verifique a situação e procure orientação das autoridades.",
            "modo": "FALLBACK"
        }

    carregar_modelo()

    situacao = SITUACOES[categoria]

    prompt = (
        "Complete the safety advice.\n"
        "Situation: A tree has fallen across the road.\n"
        "Advice: Stay away from the fallen tree.\n\n"
        f"Situation: {situacao}\n"
        "Advice:"
    )

    try:
        entradas = tokenizer(prompt, return_tensors="pt")

        with torch.no_grad():
            saida = modelo.generate(
                **entradas,
                max_new_tokens=80,
                do_sample=False
            )

        resposta = tokenizer.decode(
            saida[0],
            skip_special_tokens=True
        ).strip()

        return {
            "orientacao_gerada": resposta,
            "idioma_gerado": "en",
            "orientacao_segura": ORIENTACOES_SEGURAS[categoria],
            "modo": "FLAN_T5_LOCAL" if resposta else "FALLBACK"
        }

    except Exception as erro:
        print(f"Erro na geração: {erro}")

        return {
            "orientacao_gerada": "",
            "idioma_gerado": "en",
            "orientacao_segura": ORIENTACOES_SEGURAS[categoria],
            "modo": "FALLBACK"
        }
