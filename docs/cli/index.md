# CLI Tools

*rhoknp* provides a command-line interface (CLI).

## serve

The `serve` command starts a web server to provide a playground for the given language analyzer.

```{eval-rst}
.. prompt::
    :prompts: $

    rhoknp serve {jumanpp|knp|kwja} [--host HOST] [--port PORT]
```

```{note}
To use the `serve` command, install *rhoknp* with the following command:

```{eval-rst}
.. prompt::
     :prompts: $

     pip install rhoknp[serve]
```

## show

The `show` command shows the given KNP file in a tree format.

```{eval-rst}
.. prompt::
    :prompts: $

    rhoknp show <PATH-TO-KNP-FILE> [--pos] [--rel]
```

## stats

The `stats` command shows the statistics of the given KNP file.

```{eval-rst}
.. prompt::
    :prompts: $

    rhoknp stats <PATH-TO-KNP-FILE> [--json]
```