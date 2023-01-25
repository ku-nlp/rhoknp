try:
    import rhoknp.cli.cli
    import rhoknp.cli.serve
    import rhoknp.cli.show
    import rhoknp.cli.stats  # noqa: F401
except ImportError as e:
    raise ImportError(
        f"{e.msg}\nExtra dependencies are required to use the CLI. Install it with `pip install rhoknp[cli]`."
    )
