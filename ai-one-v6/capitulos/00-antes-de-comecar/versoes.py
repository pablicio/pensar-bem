import sys

import numpy
import pandas
import scipy
import sklearn
import torch

print("Python", sys.version.split()[0])
print("NumPy", numpy.__version__)
print("pandas", pandas.__version__)
print("SciPy", scipy.__version__)
print("scikit-learn", sklearn.__version__)
print("PyTorch", torch.__version__)
print("núcleos do PyTorch:", torch.get_num_threads())
