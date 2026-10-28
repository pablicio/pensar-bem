import time

import numpy as np
import onnxruntime as ort

opcoes = ort.SessionOptions()
opcoes.intra_op_num_threads = 1      # um núcleo, como celular
foto = np.zeros((1, 3, 128, 128), dtype=np.float32)
for arquivo in ("resnet.onnx", "resnet_int8.onnx",
                "mobilenetv3.onnx"):
    sessao = ort.InferenceSession(
        arquivo, opcoes, providers=["CPUExecutionProvider"])
    for _ in range(5):
        sessao.run(None, {"foto": foto})
    inicio = time.perf_counter()
    for _ in range(50):
        sessao.run(None, {"foto": foto})
    ms = (time.perf_counter() - inicio) / 50 * 1000
    print(f"{arquivo:18} {ms:5.1f} ms por foto")
