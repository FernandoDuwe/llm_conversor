# llm_conversor

Documentador para IA

## Instalação

A aplicação rodará em um container Docker, sendo necessarío o seguinte comando para instalação

Instalar a imagem do Python e as dependências necessárias

```sh
docker compose up -d
```

## Ollama - Baixando o modelo correspondente

O modelo Ollama rodará localmente, para isso, o modelo deve ser baixado no container:

```sh
docker exec -it ollama ollama pull nomic-embed-text

docker exec -it ollama ollama pull qwen2.5-coder:0.5b


```
