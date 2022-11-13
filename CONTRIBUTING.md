# Contributing

## Formatting python code

This repository uses [autopep8](https://pypi.org/project/autopep8/) to format Python code with its default settings.

To install autopep8, ensure you have python and pip installed and run `pip install autopep8`. This install autopep8 globally to your system.

Format code by running:

```sh
autopep8 */*.py -i -aaaa
```

The formatting is checked with [pycodestyle](https://pypi.org/project/pycodestyle/). To install it, run `pip3 install pycodestyle`.

Check formatting by running:

```sh
pycodestyle .
```

## Formatting other code

This repository uses [Prettier](https://prettier.io/) to format code with its default settings.

To install Prettier, ensure you have Nodejs and npm installed and run `sudo npm i -g prettier`. This install prettier globally to your system.

Format code by running:

```sh
prettier . --write
```

Check formatting by running:

```sh
prettier . --check
```

## Run acceptance tests

To execute acceptance tests with docker-compose, run:

```sh
docker-compose -f docker-compose.test.yml up --exit-code-from test
```

Note that tests except empty database. To clean up test database volume after execution, run:

```sh
docker-compose -f docker-compose.test.yml down -v
```
