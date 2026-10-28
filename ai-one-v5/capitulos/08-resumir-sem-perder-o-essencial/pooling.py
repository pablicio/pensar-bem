import torch
import torch.nn.functional as F

x = torch.tensor([[1., 3., 2., 0.],
                  [4., 6., 1., 1.],
                  [0., 2., 5., 7.],
                  [1., 1., 3., 2.]], requires_grad=True)
maior = F.max_pool2d(x[None, None], 2)[0, 0]
media = F.avg_pool2d(x[None, None], 2)[0, 0]
print("máximo de cada bloco 2×2:")
print(maior.detach())
print("média de cada bloco 2×2:")
print(media.detach())

maior.sum().backward()       # o gradiente de cada saída é 1
print("gradiente do máximo, de volta na entrada:")
print(x.grad)
