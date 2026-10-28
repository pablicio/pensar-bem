FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive LANG=C.UTF-8
RUN apt-get update && apt-get install -y --no-install-recommends \
      binutils-riscv64-linux-gnu gcc-riscv64-linux-gnu \
      qemu-user gdb-multiarch \
    && rm -rf /var/lib/apt/lists/*
COPY --chmod=755 roda display depura /usr/local/bin/
WORKDIR /livro
