# Contributing

Thank you for your interest in improving *rhoknp*!
We give an overview on contributing to the *rhoknp* project.

## Development Environment

Development should be done using the latest version of Python.
As of this writing, it is Python 3.10.

Install the development dependencies using [poetry](https://python-poetry.org/).

```{eval-rst}
.. prompt::
    :prompts: $

    poetry install
    pre-commit install
```

## Submitting a Pull Request

Before submitting a pull request, run lints and test.

```{eval-rst}
.. prompt::
    :prompts: $

    poetry run pre-commit run --all-files
    poetry run pytest
```

## Testing

If you are adding a new feature, please add a test for it.
When the feature is large, first open an issue to discuss the idea.

If you are fixing a bug, please add a test that exposes the bug and fails before applying your fix.
