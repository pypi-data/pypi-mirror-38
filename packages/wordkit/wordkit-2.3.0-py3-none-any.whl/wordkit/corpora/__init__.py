"""Corpora."""
from .celex import Celex
from .cmudict import CMU
from .deri import Deri
from .merge import merge
from .subtlex import Subtlex
from .lexique import Lexique
from .bpal import BPal
from .wordnet import WordNet
from .lexiconproject import LexiconProject
from .base import Reader

__all__ = ["Celex",
           "CMU",
           "Deri",
           "merge",
           "Subtlex",
           "BPal",
           "Lexique",
           "WordNet",
           "LexiconProject",
           "Reader"]
