# AI One, volume 6 — a imagem do leitor e do conferidor.
#   docker build -t ai-one:v6 books/ai-one-v6/tools
# Versões fixadas em 18/10/2026 (PyPI), no dia em que a escrita deste
# volume começou; registradas no ROTEIRO.md.
FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONHASHSEED=0 \
    MPLBACKEND=Agg OMP_NUM_THREADS=4 MKL_NUM_THREADS=4
# PyTorch só para CPU, do índice oficial (sem as bibliotecas de CUDA).
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu \
    torch==2.14.1
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
WORKDIR /projeto
