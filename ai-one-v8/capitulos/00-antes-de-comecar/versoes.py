import sys

import matplotlib
import numpy
import pandas
import sklearn
import tokenizers
import torch
import transformers

print("Python", sys.version.split()[0])
print("NumPy", numpy.__version__)
print("pandas", pandas.__version__)
print("scikit-learn", sklearn.__version__)
print("matplotlib", matplotlib.__version__)
print("tokenizers", tokenizers.__version__)
print("transformers", transformers.__version__)
print("PyTorch", torch.__version__)
print("núcleos do PyTorch:", torch.get_num_threads())
