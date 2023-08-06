# PyCodeExec
Simple python library that can execute arbitrary code from supported programming languages.

# Usage

### Synchronous JavaScript 
```python
from pycodeexec import Runner

javascript = Runner("javascript")
output = javascript.get_output("console.log([...Array(10)].map(i=>i*i))")

print(output) 
# [ 0, 1, 4, 9, 16, 25, 36, 49, 64, 81 ]
```

### Also supports Asyncio
```python
from pycodeexec.asyncio import Runner

javascript = Runner("javascript")
await javascript.is_ready()
output = await javascript.get_output("console.log([...Array(10)].map(i=>i*i))")

print(output)
# [ 0, 1, 4, 9, 16, 25, 36, 49, 64, 81 ]

```

# Supported Languages
* Python
* JavaScript
* Ruby
* C
* More to come

# Installation
```bash
pip install pycodeexec
```