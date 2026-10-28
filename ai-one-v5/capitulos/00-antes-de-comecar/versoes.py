import sys

import numpy
import PIL
import scipy
import torch
import torchvision

print("Python", sys.version.split()[0])
print("NumPy", numpy.__version__, "· SciPy", scipy.__version__)
print("Pillow", PIL.__version__)
print("PyTorch", torch.__version__)
print("torchvision", torchvision.__version__)
print("núcleos usados pelo PyTorch:", torch.get_num_threads())
