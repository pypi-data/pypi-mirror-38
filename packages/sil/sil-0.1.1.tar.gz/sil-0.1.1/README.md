# About
Sil helps keep track of an iterative functions status inline.

```
from sil import Sil

status = Sil(total=num_el)
for i, el in elements:
  sil.update(i)


status = Sil(total=num_el)
for el in elements:
  status.tick()
```


## How to install with conda

```
pip install sil

# remove old copies
rm -rf /anaconda3/lib/python3.6/site-packages/sil*

conda skeleton pypi sil
conda build sil
conda install --use-local sil
```
