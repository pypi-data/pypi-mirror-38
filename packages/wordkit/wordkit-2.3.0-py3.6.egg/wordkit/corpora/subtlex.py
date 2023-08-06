"""Corpus readers for Subtlex."""
from .base import Reader

# Currently redundant, but useful for future-proofing.
language2field = {"eng-uk": {"orthography": "Spelling",
                             "frequency": "FreqCount"},
                  "eng-us": {"orthography": "Word",
                             "frequency": "FREQcount"},
                  "nld": {"orthography": "Word",
                          "frequency": "FREQcount"},
                  "deu": {"orthography": "Word",
                          "frequency": "WFfreqCount"},
                  "chi": {"orthography": "Word",
                          "frequency": "WCount"}}

ALLOWED_LANGUAGES = set(language2field.keys())


class Subtlex(Reader):
    """
    Reader for the various Subtlex corpora.

    These are corpora of frequency norms which explain significantly more
    variance than other frequency norms based on large corpora.

    In general, all the Subtlex corpora are associated with a paper.
    For an overview, visit:
        http://crr.ugent.be/programs-data/subtitle-frequencies

    Please make sure to read the associated articles, and cite them whenever
    you use a version of Subtlex!

    This class can read both the Excel and csv versions of the subtlex files.
    If you can, please consider converting the Excel files offered by the
    original authors to a csv before processing as this will significantly
    speed up the entire process.

    Parameters
    ----------
    path : string
        The path to the file. The extension of this file will be used to
        determine the method we use to open the file.
    fields : tuple, default ("orthography", "frequency")
        The fields to retrieve from this corpus.
    language : string, default "eng-uk"
        The language the corpus is in.

    """

    def __init__(self,
                 path,
                 fields=("orthography", "frequency"),
                 language="eng-uk",
                 merge_duplicates=True,
                 scale_frequencies=False):
        """Initialize the subtlex reader."""
        if language not in ALLOWED_LANGUAGES:
            raise ValueError("Your language {}, was not in the set of "
                             "allowed languages: {}".format(language,
                                                            ALLOWED_LANGUAGES))
        if language == "chi":
            skiprows = 2
        else:
            skiprows = 0
        super().__init__(path,
                         fields,
                         language2field[language],
                         language,
                         merge_duplicates=merge_duplicates,
                         diacritics=None,
                         scale_frequencies=scale_frequencies,
                         sep="\t",
                         skiprows=skiprows)
