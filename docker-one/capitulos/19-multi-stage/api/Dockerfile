FROM python:3.13-slim AS builder
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential libpq-dev \
 && rm -rf /var/lib/apt/lists/*
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.13-slim
RUN apt-get update \
 && apt-get install -y --no-install-recommends libpq5 \
 && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" PYTHONUNBUFFERED=1
RUN useradd --create-home --uid 10001 app
WORKDIR /app
COPY --chown=app:app . .
USER app
EXPOSE 8000
CMD ["uvicorn", "main:app", \
     "--host", "0.0.0.0", "--port", "8000"]
