# citrine-python
Python library for the Citrine Platform

## Installation
Clone from github:
```bash
git clone git@github.com:CitrineInformatics/citrine-python
```

Create a virtual environment using Python >= 3.6, and install requirements:
```bash
pip install -U -r requirements.txt
pip install -U -r test_requirements.txt
```

## Documentation

The documentation for this project is built using [Sphinx](http://www.sphinx-doc.org/en/master/).

### Building documentation

To build the documentation for this project, make sure you've installed all dependencies (core
and development) using pipenv. Once done:

```
cd docs/
make html
```

You can see the result by opening `docs/_build/html/index.html` in a web browser.

### Autogenerated docs

Sphinx supports generating documentation from docstrings, which is accomplished automatically
during the build step using sphinxcontrib-apidoc. The output of this process is stored in the gitignore'd
`docs/source/reference` directory. It's not stored in source control because it's generated from
the current state of the docstrings in the source code.

### Custom documentation

One of the outstanding features of sphinx is its support for arbitrarily organized documentation
materials such as tutorials, introductions, and other context providing content. These items should
be stored in source control under the `docs/source` directory in properly formatted `.rst` files.

## Logging

A number of our python modules use python's built-in `logging` module, which supports several log
levels:

* `FATAL` - indicates a very serious (probably irrecoverable) failure has occurred
* `ERROR` - indicates an error which by default will not be handled has occurred
* `WARNING` - indicates that something unusual is happening, often precedes failures
* `INFO` - informational output unrelated to problems
* `DEBUG` - verbose information output that may assist the developer while debugging
* `NOTSET` - no filtering whatsoever

Each log level includes the previous, i.e. `WARNING` includes itself, `ERROR`, and `FATAL`. By
default, the log level is set to `INFO`. However, it may be preferable to set the log level to
`WARNING` or `ERROR` if your program's output should be concise and/or only produce actionable
information. When debugging issues, increasing the verbosity to `DEBUG` may be helpful,
particularly if seeking assistance from the Citrine team.

To set your log level, add
```python
import logging
logging.root.setLevel(level=logging.DEBUG)
```
with the desired log level to your script.

### Fine-grained log level control

In some scenarios, you may wish to increase or decrease the verbosity of a particular logger. For
instance

```python
from taurus.entity.dict_serializable import logger
import logging
logger.setLevel(logging.ERROR)
```
will silence warnings about receiving superfluous data in responses from Citrine APIs, while still
allowing other loggers to produce output of `WARNING` level and lower.

Another example:
```python
import logging
import logging
citrine._session.logger.setLevel(logging.DEBUG)
```
will enable `DEBUG` level output in the for all activity relating to HTTP requests to Citrine APIs.

In general, all log output originating from Citrine source code will include the module from which
log output originates. By convention loggers are named `logger`, so the module + `.logger` will
locate the correct instance, e.g. the log line

```
INFO:citrine._session:200 GET /projects/fc568490-224a-4070-807f-1427c4f4dcd8
```
is an example of output from the logger in the previous example.
