# llm_conversor

Documentador para IA

## Instalação

A aplicação roda em containers Docker. O arquivo base `docker-compose.yml` foi deixado **compatível com Windows**, evitando o erro de dispositivo inexistente como `/dev/dri`.

Suba os serviços com:

```sh
docker compose up -d --build
```

### Intel GPU / Intel AI Boost (NPU)

Para usar passthrough de **Intel GPU** e **Intel NPU** em um **host Linux** com os devices expostos, utilize também o override:

```sh
docker compose -f docker-compose.yml -f docker-compose.intel-linux.yml up -d --build
```

Esse arquivo adicional expõe:

- `INTEL_GPU_DEVICE` → padrão `/dev/dri`
- `INTEL_NPU_DEVICE` → padrão `/dev/accel`

Exemplo:

```powershell
$env:INTEL_GPU_DEVICE="/dev/dri"
$env:INTEL_NPU_DEVICE="/dev/accel"
docker compose -f docker-compose.yml -f docker-compose.intel-linux.yml up -d --build
```

> **Importante:** em **Windows/Docker Desktop**, `/dev/dri` normalmente não existe. Nessa plataforma, o compose base deve ser usado sem o override Linux. O uso efetivo da NPU em container depende de suporte específico de driver/runtime.

## Ollama - Baixando o modelo correspondente

O modelo Ollama rodará localmente, para isso, o modelo deve ser baixado no container:

```sh
docker exec -it ollama ollama pull nomic-embed-text

docker exec -it ollama ollama pull qwen2.5-coder:0.5b

```

## Executar container

```sh
docker exec -it llm_conversor-python_app-1 /bin/bash

```
