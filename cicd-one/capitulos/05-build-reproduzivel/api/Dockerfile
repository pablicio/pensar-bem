FROM python:3.12.9-slim-bookworm AS build
RUN apt-get update \
 && apt-get install -y --no-install-recommends libgeos-dev \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --require-hashes \
    --prefix=/instalado -r requirements.txt

FROM python:3.12.9-slim-bookworm
RUN apt-get update \
 && apt-get install -y --no-install-recommends libgeos-c1v5 \
 && rm -rf /var/lib/apt/lists/*
COPY --from=build /instalado /usr/local
WORKDIR /app
COPY app/ app/
USER nobody
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
