FROM python:3.13-slim
ENV PYTHONHASHSEED=0 MPLBACKEND=Agg OMP_NUM_THREADS=4 \
    HF_HUB_OFFLINE=1
# o PyTorch só para processador, do índice oficial
RUN pip install --no-cache-dir \
    --index-url https://download.pytorch.org/whl/cpu \
    torch==2.14.1
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
WORKDIR /projeto
