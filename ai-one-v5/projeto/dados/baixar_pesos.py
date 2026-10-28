"""Os pesos pré-treinados que o livro usa, baixados uma vez."""
from torchvision import models
from torchvision.models import detection

PESOS = [
    (models.resnet18, "IMAGENET1K_V1"),
    (models.mobilenet_v3_small, "IMAGENET1K_V1"),
    (models.efficientnet_b0, "IMAGENET1K_V1"),
    (detection.fasterrcnn_mobilenet_v3_large_fpn, "COCO_V1"),
]

for construtor, pesos in PESOS:
    modelo = construtor(weights=pesos)
    n = sum(p.numel() for p in modelo.parameters())
    print(f"{construtor.__name__:34} {n:>11,} parâmetros")
