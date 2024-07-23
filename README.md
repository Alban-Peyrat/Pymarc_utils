# Pymarc utils

[![Active Development](https://img.shields.io/badge/Maintenance%20Level-Actively%20Developed-brightgreen.svg)](https://gist.github.com/cheerfulstoic/d107229326a01ff0f333a1d3476e068d)

A set of functions to handle data using [Python `pymarc` library](https://pypi.org/project/marc/) :

* `marc_utils_4.py` using version 4.2.2 of the library
* `marc_utils_5.py` using version 5.2.0

Incompatible changes from `marc_utils_4.py` to `marc_utils_5.py` :

* `__sort_subfields()` parameter `curr_subf` was renammed to `subf_list`
* `force_indicators` :
  * Parameter `indicators` (list of strings, defaulted to `[" ", " "]`) was changed to become two parameter `ind1` & `ind2`, both `str` defaulted to `None`
  * Now, if their value is set to `None` (default behaviour), keeps their current value (before, default behaviour was to write to a blank and it could not be used to keep the field current indicators)

_See [`pymarc` releases in the GitLab repository](https://gitlab.com/pymarc/pymarc/-/releases) for important changes in the library._