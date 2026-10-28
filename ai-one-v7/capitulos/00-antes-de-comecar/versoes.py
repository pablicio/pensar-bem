import sys

import matplotlib
import numpy
import PIL
import scipy
import sklearn
import torch

print("Python", sys.version.split()[0])
print("NumPy", numpy.__version__)
print("SciPy", scipy.__version__)
print("scikit-learn", sklearn.__version__)
print("matplotlib", matplotlib.__version__)
print("Pillow", PIL.__version__)
print("PyTorch", torch.__version__)
print("núcleos do PyTorch:", torch.get_num_threads())
