import torch
from torchvision.ops import box_iou

from folha.caixas import da_mascara, do_conjunto, iou
from folha.caixas import para_cantos, para_centro

a = torch.tensor([[10.0, 10, 50, 40]])     # x0, y0, x1, y1
b = torch.tensor([[30.0, 20, 70, 60], [60.0, 50, 90, 80]])
print("a em centro:", para_centro(a).tolist())
print("e de volta:", para_cantos(para_centro(a)).tolist())
print("IoU à mão:      ", iou(a, b).numpy().round(4))
print("IoU torchvision:", box_iou(a, b).numpy().round(4))

caixas = do_conjunto()
foto = "1"
print(f"\nfoto {foto}: {len(caixas[foto])} lesões"
      " no caixas.csv")
mascara = da_mascara(foto)
print("caixas da máscara iguais às do csv:",
      torch.equal(mascara, caixas[foto]))
m = iou(caixas[foto], caixas[foto])
print("IoU entre as lesões da foto 1:")
print(m.numpy().round(2))
