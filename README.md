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

If you are first time running this program, execute the below first

```bash
pip install -r requirements-dev.txt
```

------

Check `test_run()` in `msnmetrosim/views/simulate` for the example usage.

- Documentation and APIs currently not fully developed, even a prototype or a draft.

### Environment Variables

`TEST_PERFORMANCE_TOLERANCE`

- This is **optional**. You only need this if you are running the tests.

- This determines the performance test tolerance in terms of time.

- More information can be found in `tests/conftest.py`.
