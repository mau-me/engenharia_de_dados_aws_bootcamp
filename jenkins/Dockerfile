# Use a imagem base do Jenkins
FROM jenkins/jenkins

# Troque para o usuário root para instalar pacotes
USER root

# Atualize os repositórios e instale o pip do Python
RUN apt-get update && \
    apt-get install -y python3-pip && \
    apt-get install -y python3-venv

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Crie um ambiente virtual
RUN python3 -m venv venv

# Instale os pacotes Python listados no requirements.txt
RUN venv/bin/pip3 install --no-cache-dir -r requirements.txt

# Altere de volta para o usuário Jenkins
USER jenkins