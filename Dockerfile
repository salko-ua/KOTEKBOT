FROM python:3.11-slim AS poetry

ENV PATH "/root/.local/bin:${PATH}"
ENV PYTHONUNBUFFERED 1

WORKDIR /root
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN apt-get update && \
    apt-get install curl -y --no-install-recommends && \
    curl -sSL https://install.python-poetry.org | python -
COPY poetry.lock pyproject.toml ./
RUN poetry export --no-interaction -o requirements.txt --without-hashes --only main,docker


FROM python:3.11-slim AS base

ENV PYTHONPATH "/app"

WORKDIR /app

RUN groupadd -g 5000 container && useradd -d /app -m -g container -u 5000 container
COPY --from=poetry /root/requirements.txt ./
RUN pip --no-cache-dir install -U pip && \
    pip --no-cache-dir install -r requirements.txt
COPY src/ src/

FROM base AS final

RUN chown -R 5000:5000 /app
USER container

CMD ["dumb-init", "python", "-m", "src"]
