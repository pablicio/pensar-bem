FROM python:3.13-slim
ENV PYTHONHASHSEED=0 MPLBACKEND=Agg OMP_NUM_THREADS=4
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
WORKDIR /projeto
