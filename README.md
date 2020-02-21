# citrine-python
Python library for the Citrine Platform

## Installation and Development
Clone from github:
```bash
git clone git@github.com:CitrineInformatics/citrine-python
```

Create a virtual environment using Python >= 3.6.
One option is to use conda, but it is not required.

```bash
conda create -n <environment_name> python=3.7
conda activate <environment_name>
```

Then install requirements.

```bash
pip install -U -r requirements.txt
pip install -U -r test_requirements.txt
pip install --no-deps -e .
```

Note that if you use `python setup.py install` it will **not** install the libraries in "test_requirements.txt".
Although not necessary for *using* citrine-python, these libraries are important for development.

If using a conda environment, you can now launch a Jupyter notebook from the environment with `jupyter notebook`.
The resulting notebook will have access to the citrine-python library and all its dependencies.

Changes to citrine-python must pass all tests, follow style guidelines, and maintain 100% test coverage.
We use flake8 as a linter.
To run the linter on the "src/" directory:
```bash
flake8 src
```

### Running tests

We use pytest to run tests and use the associated library pytest-cov to check coverage.
See the [PyTest documentation](https://docs.pytest.org/en/latest/usage.html) for more information.

#### Command line

To run all tests and output a report of the coverage of the "src/" directory:
```bash
run pytest tests/ --cov=src/
```

It is not uncommon to have path issues when running pytest from the command line.
Ensure that your $PATH variable contains the directory with the citrine-python repo.
If that does not work and you want to run tests from the command line (as opposed to from an editor such as PyCharm) it is more reliable to use `pipenv`.
```bash
pip install pipenv
pipenv install --dev
pipenv shell
```

You can now run commands by prefacing them with `pipenv run`.
For example, `pipenv run pytest`.

To exit the pipenv shell, run `exit`.
To deactivate a conda environment, use `conda deactivate`.

#### Docker

Running tests in Docker will ensure the same development environment as used by Travis CI, our continuous integration server.
See the file .travis.yml in the repository root for more information.

To build the container, run this command from the repository root.
It will tag the image as "citrine-python":
```bash
docker build -f scripts/Dockerfile.pytest -t citrine-python .
```

To get an interactive bash shell in the Docker container, overriding the default entrypoint, run the following:
```bash
docker run --rm -it --entrypoint bash citrine-python
```

To run all unit tests in the Docker container with default parameters:
```bash
docker run --rm -it citrine-python
```

To run all tests in a module or run a specific test, run a command like the following (note that this will result a reported test coverage that is low):
```bash
docker run --rm -it citrine-python tests/serialization/test_table.py
docker run --rm -it citrine-python tests/serialization/test_table.py::test_simple_deserialization
```

## Documentation

The documentation for this project is built using [Sphinx](http://www.sphinx-doc.org/en/master/) and can be found [here](https://citrineinformatics.github.io/citrine-python/index.html).

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
* `NOTSET` - currently unused in Citrine code, typically *extremely* verbose output describing
  the details of every operation being performed

As set, a logging level will return any logs at the set level and above, e.g. `WARNING` includes
itself, `ERROR`, and `FATAL`. By default, the log level is set to `WARNING`. However, it may be
preferable to set the log level to `ERROR` if your program's output should be particularly concise
and/or only produce actionable information. When debugging issues, increasing the verbosity to `DEBUG`
may be helpful, particularly if seeking assistance from the Citrine team.

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
from citrine._session import logger
import logging
logger.setLevel(logging.DEBUG)
```
will enable `DEBUG` level output in the for all activity relating to HTTP requests to Citrine APIs.

In general, all log output originating from Citrine source code will include the module from which
log output originates. By convention loggers are named `logger`, so importing `logger` from the
originating module will locate the correct instance, e.g. the log line

```
INFO:citrine._session:200 GET /projects/fc568490-224a-4070-807f-1427c4f4dcd8
```
is an example of output from the logger in the previous example.

## Developement Status

Classes and methods may be marked as *alpha* by including `[ALPHA]` at the start of their docstrings.
These methods are intended for development, testing, and experimentation, are not supported, and may change or be removed without notice```
