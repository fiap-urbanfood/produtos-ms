FROM python:3.12-alpine

# Parametros environment
ARG USER=nonroot
ENV HOME /home/"$USER"

# Variaveis de ambiente
ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED 1

# Criar o PATH do app
RUN mkdir /deploy
RUN mkdir /deploy/logs && chmod +w /deploy/logs

# Install prerequisites
RUN apk update && apk upgrade
RUN apk add curl \
            bash \
            netcat-openbsd \
            vim \
            less \
            net-tools \
            procps \
            bind-tools \
            tcpdump \
    && apk cache clean

# Config Timezones
RUN apk add tzdata --no-cache \
  && cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime \
  && echo "America/Sao_Paulo" > /etc/timezone

# MySQL Connector
RUN apk add --no-cache mysql mysql-client mariadb-connector-c-dev ;\
    apk add --no-cache --virtual .build-deps \
    build-base \
    mariadb-dev ;\
    pip install mysqlclient;\
    apk del .build-deps \
    && apk cache clean

# Add User
RUN adduser -D "$USER" \
  && mkdir -p /etc/sudoers.d \
  && echo "$USER ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/"$USER" \
  && chmod 0440 /etc/sudoers.d/"$USER"

# Defina o diretório do APP
USER "$USER"
WORKDIR $HOME/app

# Create Path Log Application
RUN mkdir -p $HOME/app/log

# Copia os arquivos do projeto
COPY --chown="$USER:$USER" --chmod=750 *.py $HOME/app
COPY --chown="$USER:$USER" --chmod=750 pytest.ini $HOME/app
COPY --chown="$USER:$USER" --chmod=750 requirements.txt $HOME/app

# Copia os diretorios do projeto
COPY --chown="$USER:$USER" --chmod=755 api  $HOME/app
COPY --chown="$USER:$USER" --chmod=755 core $HOME/app
COPY --chown="$USER:$USER" --chmod=755 tests $HOME/app
COPY --chown="$USER:$USER" --chmod=755 models  $HOME/app
COPY --chown="$USER:$USER" --chmod=755 schemas $HOME/app

# Upgrade pip
RUN pip3 install --upgrade pip --user

# Instala as dependencias
RUN pip3 install -r requirements.txt

RUN chmod -R 750 ./main.py

# Sobe o backend
EXPOSE 8003
STOPSIGNAL SIGINT
ENTRYPOINT ["python", "main.py"]
CMD ["python", "criar_tabelas.py"]
