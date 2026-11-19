# 🚨 AlertaCom-IA

## 📌 Sobre o projeto

O **AlertaCom-IA** é um projeto acadêmico desenvolvido para auxiliar na identificação de incidentes urbanos por meio de inteligência artificial e visão computacional.

A solução permite que o usuário envie uma fotografia de uma situação urbana, que será analisada por um modelo de inteligência artificial capaz de classificá-la em diferentes categorias.

O objetivo é demonstrar como tecnologias de visão computacional podem contribuir para o monitoramento de problemas urbanos.

## 🎯 Objetivos

- Identificar possíveis incidentes urbanos a partir de fotografias.
- Classificar imagens utilizando inteligência artificial.
- Disponibilizar uma API REST para envio e análise de imagens.
- Demonstrar a aplicação prática de visão computacional.
- Explorar as possibilidades e limitações de modelos de IA.

## 🛠️ Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Desenvolvimento da aplicação |
| FastAPI | Construção da API REST |
| Swagger UI | Documentação e testes da API |
| PyTorch | Execução do modelo de IA |
| Transformers | Carregamento e utilização do CLIP |
| CLIP | Classificação de imagens |
| Pillow | Processamento de imagens |
| Google Gemini | Integração experimental com IA generativa |

## 🧠 Inteligência artificial

O projeto utiliza o modelo **openai/clip-vit-base-patch32**, executado localmente.

O CLIP é um modelo de visão computacional capaz de relacionar imagens e descrições textuais.

No AlertaCom-IA, cada categoria possui uma descrição textual em inglês. O modelo compara a fotografia enviada com essas descrições e seleciona a categoria com maior pontuação relativa.

### Categorias reconhecidas

| Categoria | Descrição |
|---|---|
| `ALAGAMENTO` | Ruas alagadas |
| `BUEIRO_OBSTRUIDO` | Bueiros obstruídos por resíduos |
| `ARVORE_CAIDA` | Árvores caídas em vias públicas |
| `BURACO_NA_VIA` | Buracos no asfalto |
| `SEM_INCIDENTE` | Ruas sem incidentes visíveis |

### Funcionamento da classificação

1. O usuário envia uma imagem para a API.
2. O sistema verifica o arquivo recebido.
3. A imagem é processada pelo Pillow.
4. O modelo CLIP compara a imagem com as descrições das categorias.
5. A categoria com maior pontuação relativa é selecionada.
6. A API retorna o resultado em formato JSON.

**Observação:** a pontuação relativa não representa uma probabilidade calibrada de acerto. Ela indica a preferência do modelo entre as categorias disponíveis.

## 🔌 Endpoints da API

### GET `/`

Retorna informações básicas sobre o projeto.

### GET `/health`

Verifica se a API está funcionando.

Exemplo de resposta:

```json
{
  "status": "online"
}
```

### POST `/analyze-incident`

Recebe uma imagem e realiza sua classificação.

**Entrada:** arquivo de imagem enviado como `multipart/form-data`.

**Exemplo de resposta:**

```json
{
  "imagem_valida": true,
  "modo": "CLIP_LOCAL",
  "categoria": "BURACO_NA_VIA",
  "pontuacao_relativa": 0.9997,
  "modelo": "openai/clip-vit-base-patch32"
}
```

O exemplo representa um dos testes realizados durante o desenvolvimento.

## 🧪 Testes realizados

Foram realizados testes com cinco fotografias representando diferentes situações urbanas.

| Teste | Categoria esperada | Resultado |
|---|---|---|
| 1 | ALAGAMENTO | Correto |
| 2 | SEM_INCIDENTE | Correto |
| 3 | BUEIRO_OBSTRUIDO | Correto |
| 4 | ARVORE_CAIDA | Correto |
| 5 | BURACO_NA_VIA | Correto |

Após a inclusão da categoria `BURACO_NA_VIA`, os cinco testes foram repetidos e apresentaram as classificações esperadas.

**Resultado observado: 5 classificações corretas em 5 imagens testadas.**

Esse resultado corresponde apenas ao conjunto de imagens utilizado durante os testes e não comprova a precisão geral do modelo.

## ▶️ Como executar o projeto

### 1. Criar o ambiente virtual

```bash
python -m venv .venv
```

### 2. Ativar o ambiente virtual

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 4. Iniciar o servidor

```bash
python -m uvicorn src.main:app --reload
```

### 5. Acessar o Swagger

Abra no navegador:

`http://127.0.0.1:8000/docs`

Selecione o endpoint `POST /analyze-incident`, envie uma fotografia e execute a análise.

Na primeira execução, o modelo CLIP poderá precisar baixar seus arquivos, exigindo conexão com a internet.

## 📁 Estrutura do projeto

```text
AlertaCom-IA/
├── src/
│   ├── main.py
│   ├── vision_classifier.py
│   └── clip_classifier.py
├── testes/
│   └── alagamento.jpeg
├── teste_clip.py
├── teste_gemini.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

O arquivo `.env` contém configurações locais e não deve ser enviado ao repositório.

## ⚠️ Limitações atuais

- O modelo CLIP realiza classificações entre categorias previamente definidas.
- A classificação depende das descrições textuais utilizadas.
- A pontuação relativa não representa uma garantia de acerto.
- O sistema ainda não realiza avaliação automática da gravidade dos incidentes.
- A análise de uma fotografia isolada não é suficiente para determinar se uma área é segura.
- São necessários testes com um conjunto maior e mais diversificado de imagens para avaliar o desempenho real da solução.

### Integração com Gemini

O projeto também explorou a integração com a API do Google Gemini.

Durante os testes, foram encontrados erros de timeout (`504 DEADLINE_EXCEEDED`).

Como alternativa, foi implementado o classificador local CLIP, permitindo realizar classificações sem depender da geração de conteúdo pelo Gemini.

O projeto mantém uma resposta de demonstração para situações em que a análise pelo Gemini não é concluída. Essa resposta não representa uma classificação realizada pela IA.

## 🔐 Segurança

As credenciais de acesso à API Gemini são armazenadas localmente no arquivo `.env`.

Esse arquivo deve permanecer excluído do versionamento por meio do `.gitignore`.

## 🎓 Contexto acadêmico

Projeto desenvolvido como parte das atividades acadêmicas da **FIAP**, com foco na aplicação de inteligência artificial, desenvolvimento de software e visão computacional para identificação de incidentes urbanos.