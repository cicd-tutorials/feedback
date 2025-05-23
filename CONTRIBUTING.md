# Contributing

## Formatting

### Python

This repository uses [autopep8](https://pypi.org/project/autopep8/) to format Python code with its default settings.

To install autopep8, ensure you have python and pip installed and run `pip install autopep8`. This install autopep8 globally to your system.

Format code by running:

```sh
autopep8 -aaar --in-place --exclude back-end/server/settings.py,*/migrations/*.py .
```

The formatting is checked with [pycodestyle](https://pypi.org/project/pycodestyle/). To install it, run `pip3 install pycodestyle`.

Check formatting by running:

```sh
pycodestyle --exclude back-end/server/settings.py,*/migrations/*.py .
```

### TF

This repository uses `tofu fmt` to format `.tf` configuration files.

Format code by running:

```sh
tofu fmt -recursive
```

Check formatting by running:

```sh
tofu fmt -check -recursive
```

### Other code

This repository uses [Prettier](https://prettier.io/) to format code with its default settings.

To install Prettier, ensure you have Nodejs and npm installed and run `npm ci`. This installs prettier to `node_modules` in this directory.

Format code by running:

```sh
npm run format
```

Check formatting by running:

```sh
npm run format:check
```

## Run acceptance tests

To execute acceptance tests with docker-compose, run:

```sh
docker compose -f docker-compose.test-host-net.yml up --exit-code-from test
```

Note that tests except empty database. To clean up test database volume after execution, run:

```sh
docker compose -f docker-compose.test-host-net.yml down -v
```
