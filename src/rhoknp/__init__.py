from importlib.metadata import version

from .rhoknp import load_jumanpp, load_knp, parse

__version__ = version("rhoknp")

__all__ = ["__version__", "parse", "load_jumanpp", "load_knp"]
