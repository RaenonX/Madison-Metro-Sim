# Madison-Metro-Sim

Madison Metro Simulator.

#### Ray's worktime

[![time tracker](https://wakatime.com/badge/github/RaenonX/Madison-Metro-Sim.svg)](https://wakatime.com/badge/github/RaenonX/Madison-Metro-Sim)

------

### Introduction

This is a project of UW Madison 2020 Fall CS 638 class.

The intended group of users of this program is its developers and technical users. 

- This specification may be changed in the future


### Usage

1. Generate a map.

    ```bash
    py main.py
    ```

2. Open the generated `map.html` file.

------

More map generating functions can be called from `msnmetrosim.views`.
   
```python
from msnmetrosim.views import *

generate_clean_map().save("my_map.html")
```

------

If you are first time running this program, execute the below first

```bash
pip install -r requirements-dev.txt
```
