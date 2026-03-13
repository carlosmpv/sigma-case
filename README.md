# SIGMA Case

Um projeto avaliativo para candidatura na SIGMA.

## Como executar?

Com o diretório de trabalho na raíz deste repositório basta executar: 

```bash
docker compose up --build
```

Basta então acessar `http://localhost` ou `http://localhost:3000`

## Como desenvolver e depurar?

Este projeto utiliza devcontainers para isolar e gerenciar suas dependencias de sistema.

https://code.visualstudio.com/docs/devcontainers/containers

Com o vscode configurado basta acessar o devcontainer com `Ctrl + Shift + p` > `Dev Containers: Rebuild and Reopen in Container`


Este projeto depende de variáveis de ambiente que são definidas no docker compose. Para executar o frontend e o backend individualmentes, são utilizados arquivos `.env` que não são persistidos no repositório.

Para obter valores padrão para as variáveis de ambiente execute:
```bash
chmod +x ./make_env.sh && ./make_env.sh
```

**Importante!**

As variáveis de ambiente configuradas aqui são pensadas para o devcontainer configurado neste projeto. Caso execute por fora do devcontainer substitua `host.docker.internal` por `localhost`

### Depurando o backend

Para o backend em Python + FastAPI o vscode está configurado para executar o depurador ao pressionar `F5`. 

É necessário no entanto que o serviço **database** esteja executando no momento: `docker compose up database`, ou clickar no play que aparece sobre os serviços listados em `compose.yml` caso a extensão **Container Tools** esteja instalada.

### Depurando o frontend

Não foi configurado o depurador para o nextjs no momento, porém para executar em modo de desenvolvimento, basta executar os serviços **server** e **database**