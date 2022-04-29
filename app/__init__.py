import os
import sys
from pathlib import Path

print("############")
print(sys.path)
sys.path.append(os.getcwd())
sys.path.append(str(Path(os.getcwd()).parent))

print("############")
print(sys.path)
