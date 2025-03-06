import torch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

file_path = "./best_output/CSI100/best_cr.pkl"
data = torch.load(file_path, map_location="cpu", weights_only=False)
print(data)