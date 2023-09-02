FROM python:3.11-slim-bookworm as basic

ARG CONTAINER_USER=app
ARG CONTAINER_UID=1000
ARG CONTAINER_GID=1000

RUN groupadd -g ${CONTAINER_GID} ${CONTAINER_USER} \
    && useradd -rm -d /home/${CONTAINER_USER} \
      -s /bin/bash  \
      -g ${CONTAINER_USER}  \
      -u ${CONTAINER_UID} ${CONTAINER_USER}

USER ${CONTAINER_USER}

RUN python3 -m pip install --user pipx \
    && python3 -m pipx install poetry

WORKDIR /app

COPY . .

ENV PATH="${PATH}:/home/${CONTAINER_USER}/.local/bin"

RUN poetry install

FROM basic as app

ENTRYPOINT ["poetry", "run", "python", "-m", "kavw_cli_jinja"]
