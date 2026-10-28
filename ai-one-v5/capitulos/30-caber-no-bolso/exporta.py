import logging
import os
import warnings

import onnxruntime as ort
import torch
from onnxruntime.quantization import (
    CalibrationDataReader, QuantType, quantize_static)
from onnxruntime.quantization.shape_inference import (
    quant_pre_process)
from torch import nn

from folha.bolso import espinha
from folha.conjunto import Folhas
from folha.emprestada import extrai, treina_cabeca
from folha.treino import fixar_semente, lotes

warnings.simplefilter("ignore")              # avisos de versão
logging.disable(logging.WARNING)
fixar_semente(0, nucleos=4)
treino, valid = Folhas("treino"), Folhas("validacao")
x, y = next(iter(lotes(valid, len(valid))))


class Calibra(CalibrationDataReader):
    """Cem fotos de treino mostram o intervalo dos valores."""

    def __init__(self):
        fotos, _ = next(iter(lotes(treino, 100)))
        self.lista = iter([{"foto": f[None].numpy()}
                           for f in fotos])

    def get_next(self):
        return next(self.lista, None)


def acerto(arquivo):
    sessao = ort.InferenceSession(
        arquivo, providers=["CPUExecutionProvider"])
    notas = sessao.run(None, {"foto": x.numpy()})[0]
    return (notas.argmax(axis=1) == y.numpy()).mean()


print("modelo                    MB   acerto")
for nome in ("ResNet-18", "MobileNetV3-S"):
    rede, n = espinha(nome)
    xt, yt = extrai(rede, treino)
    cabeca = treina_cabeca(xt, yt)
    completa = nn.Sequential(rede, cabeca).eval()
    base = nome.split("-")[0].lower()
    torch.onnx.export(completa, torch.zeros(1, 3, 128, 128),
                      f"{base}.onnx", dynamo=False,
                      input_names=["foto"],
                      output_names=["notas"],
                      dynamic_axes={"foto": {0: "n"},
                                    "notas": {0: "n"}})
    quant_pre_process(f"{base}.onnx", f"{base}_pre.onnx")
    quantize_static(f"{base}_pre.onnx", f"{base}_int8.onnx",
                    Calibra(), weight_type=QuantType.QInt8,
                    per_channel=True)
    for tipo in ("", "_int8"):
        arquivo = f"{base}{tipo}.onnx"
        mb = os.path.getsize(arquivo) / 1e6
        rotulo = f"{nome} {'int8' if tipo else 'float32'}"
        print(f"{rotulo:23} {mb:5.1f} {acerto(arquivo):8.1%}")
