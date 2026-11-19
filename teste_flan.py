
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODELO = "google/flan-t5-small"

print("Carregando tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODELO)

print("Carregando modelo...")
modelo = AutoModelForSeq2SeqLM.from_pretrained(
    MODELO,
    dtype=torch.float32
)

modelo.eval()

prompt = (
    "Complete the safety advice.\n"
    "Situation: A tree has fallen across the road.\n"
    "Advice: Stay away from the fallen tree.\n\n"
    "Situation: A street is flooded.\n"
    "Advice:"
)

print("\nGerando orientação de segurança...")

entradas = tokenizer(
    prompt,
    return_tensors="pt"
)

with torch.no_grad():
    saida = modelo.generate(
        **entradas,
        max_new_tokens=80,
        do_sample=False
    )

print("\nTokens gerados:")
print(saida[0].tolist())

print("\nResposta completa:")
print(tokenizer.decode(
    saida[0],
    skip_special_tokens=False
))

print("\nResposta final:")
print(tokenizer.decode(
    saida[0],
    skip_special_tokens=True
))
