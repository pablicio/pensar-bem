import torch
from torch import nn

torch.manual_seed(0)
conv = nn.Conv2d(3, 8, 3, padding=1, padding_mode="circular")
x = torch.randn(1, 3, 32, 32)
d = 5
with torch.no_grad():
    a = conv(torch.roll(x, d, dims=3))    # desloca e convolui
    b = torch.roll(conv(x), d, dims=3)    # convolui e desloca
    print("convolução: f(Px) = P f(x)?",
          f"{(a - b).abs().max():.1e}")
    pool = nn.MaxPool2d(2)
    for d in (2, 3):
        a = pool(torch.roll(x, d, dims=3))
        b = torch.roll(pool(x), d // 2, dims=3)
        print(f"max pooling, deslocamento {d}:",
              f"{(a - b).abs().max():.2f}")
