# Build Container Image Stage
FROM python:3.11.6 as build

WORKDIR /app

# hadolint ignore=DL3013
COPY Pipfile Pipfile.lock ./
ENV PIPENV_VENV_IN_PROJECT=1
RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir pipenv && \
    python -m pipenv install

# Runtime Container Image Stage
FROM python:3.11.6-slim

RUN apt-get update && \
    apt-get install -y libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=build /app/.venv ./.venv
COPY ./ ./

ENV PATH="/app/.venv/bin:$PATH"

# port 설정
EXPOSE 8000

# run command 설정
CMD ["sh", "-c", "python3 manage.py migrate && gunicorn --bind 0.0.0.0:8000 sara_server.asgi:application -k uvicorn.workers.UvicornWorker -w 8"]
