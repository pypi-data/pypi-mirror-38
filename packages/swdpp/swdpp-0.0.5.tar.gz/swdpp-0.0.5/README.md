# sliding window determinantal point process

## usage

```python3
import numpy as np
from swdpp.swdpp import swdpp

n = 10
r = np.arange(n * n).reshape(n, n) / (n * n)
L = r @ r.T + np.eye(n)
w = 5

rank, determinants = swdpp(w, L)
print(rank)
print(determinants)
```
