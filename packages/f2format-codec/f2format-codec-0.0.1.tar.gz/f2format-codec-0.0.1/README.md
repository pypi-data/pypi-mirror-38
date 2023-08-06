# f2format-codec

Codec registry for [`f2format`](https://github.com/JarryShaw/f2format),
a back-port compiler for Python 3.6 f-string literals.

## Installation

```sh
pip install f2format-codec
```

## Usage

Include the following encoding cookie at the top of your file (this replaces
the `UTF-8` cookie if you already have it):

```python
# -*- coding: f2format -*-
```

And then write Python 3.6 f-string literals as usual :beer:

## Acknowledgement

This project levergas APIs provided by
[`f2format`](https://github.com/JarryShaw/f2format), and concepts inspired from
[`future-fstrings`](https://github.com/asottile/future-fstrings).
