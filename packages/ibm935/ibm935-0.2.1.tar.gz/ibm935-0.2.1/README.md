![version](https://img.shields.io/pypi/v/ibm935.svg) ![license](https://img.shields.io/pypi/l/ibm935.svg)

# IBM935
The codec `ibm935` is not yet officially supported. This package is designed for conversion between `unicode` and `ibm935`.

## Installation
Using `pip`:
```bash
$ pip install ibm935 
```

Or manually download the archive and run the command after extracting the stuff inside:
```bash
$ python setup.py install
```

## Usage
Before using this codec, import the module: 
```python
import ibm935
```

Then we can convert `unicode` strings into `ibm935` codec as usual:
```python
# Python 2
encoded_bytes = u"我爱Python这么美好的语言！".encode("ibm935")
decoded_string = encoded_bytes.decode("ibm935")

# Python 3 - the prefix `u` can be omitted
encoded_bytes = "我爱Python这么美好的语言！".encode("ibm935")
decoded_string = encoded_bytes.decode("ibm935")
``` 

We can also write files using this codec:
```python
with open("ibm935.txt", "w", encoding="ibm935") as f:
    f.write("我爱Python！")
```

Note:
* This package is not yet fully tested.
* There is a tough situation where writing a file with separate `words`(double-byte) causes redundant bytes like `\x0f\x0e`.
