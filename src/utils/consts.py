import os

MODEL_TYPE_OLLAMA = "qwen2.5-coder:0.5b"  # "llama3.2:3b" # "llama3.1:8b"
MODEL_TYPE_OLLAMA_EMBEDDINGS = "nomic-embed-text"

# Files
FILE_CONFIG_PROMPT = "./config/prompt.txt"

# Prompts
PROMPT_USER = "Quais são os requisitos técnicos e fórmulas descritas neste código: "

# Path
PATH_INPUT = "./input"
PATH_OUTPUT = "./output"
PATH_OLLAMA = os.getenv("OLLAMA_API_BASE_URL") or os.getenv("OLLAMA_HOST") or "http://localhost:11434"

# Temperature
TEMPERATURE_LOW_CREATIVITY = 0.1 # temperatura baixa = baixa criatividade do modelo
TEMPERATURE_BALANCED = 0.5 # temperatura equilibrada para melhor qualidade

# Generation parameters
MAX_NEW_TOKENS_SHORT = 512  # Para respostas curtas
MAX_NEW_TOKENS_MEDIUM = 1024  # Para respostas médias
MAX_NEW_TOKENS_LONG = 2048  # Para respostas longas
TOP_P = 0.5 # Para diversidade controlada nas respostas
TOP_K = 50  # Limita tokens a considerar