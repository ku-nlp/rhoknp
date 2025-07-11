# Contributing

Thank you for your interest in improving _rhoknp_!
We give an overview on contributing to the _rhoknp_ project.

## Development Environment

Development should be done using the latest version of Python.
As of this writing, it is Python 3.10.

Install the development dependencies using [uv](https://docs.astral.sh/uv/).

```{eval-rst}
.. prompt::
    :prompts: $

    uv sync
    pre-commit install
```

## Submitting a Pull Request

Before submitting a pull request, run lints and test.

```{eval-rst}
.. prompt::
    :prompts: $

    uv run pre-commit run --all-files
    uv run pytest
```

## Testing

If you are adding a new feature, please add a test for it.
When the feature is large, first open an issue to discuss the idea.

If you are fixing a bug, please add a test that exposes the bug and fails before applying your fix.
