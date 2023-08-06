"""Readers for lexicon project corpora."""
from .base import Reader


ALLOWED_LANGUAGES = ("eng-uk", "eng-us", "fra", "nld", "chi")
LANG_SEP = {"eng-uk": "\t", "nld": "\t", "eng-us": ","}
language2field = {"nld": {"orthography": "spelling"},
                  "eng-uk": {"orthography": "spelling"},
                  "eng-us": {"orthography": "Word", "rt": "I_Mean_RT"},
                  "fra": {"orthography": "item"},
                  "chi": {"orthography": "Character", "rt": "RT"}}


class LexiconProject(Reader):
    """
    Lexicon projects are a set of corpora which contain Reaction Time
    measurements for large sets of words.

    All lexicon projects can be found here:
    http://crr.ugent.be/programs-data/lexicon-projects

    If you use a lexicon project, please cite the appropriate paper.

    Parameters
    ----------
    path : string
        The path to the corpus this reader has to read.
    fields : iterable
        An iterable of strings containing the fields this reader has
        to read from the corpus.
    language : string
        The language of the corpus.

    Example
    -------
    >>> from string import ascii_lowercase
    >>> def freq_alpha(x):
    >>>     a = set(x['orthography']) - set(ascii_lowercase)
    >>>     b = x['frequency'] > 10
    >>>     return (not a) and b
    >>>
    >>> r = Reader("/path/",
    >>>            ("orthography", "frequency"),
    >>>            "eng")
    >>> words = r.transform(filter_function=freq_alpha)

    """
    def __init__(self,
                 path,
                 fields=("orthography", "rt"),
                 language='eng-uk'):
        """Initialize the reader."""
        if language not in language2field:
            langs = set(language2field.keys())
            raise ValueError("Your language {}, was not in the set of "
                             "allowed languages: {}".format(language,
                                                            langs))
        super().__init__(path,
                         fields,
                         language2field[language],
                         language,
                         merge_duplicates=False,
                         sep=LANG_SEP.get(language, None))
