import pandas as pd
import numpy as np


def process_strings(strings: pd.Series) -> pd.Series:
    """Cleaning list of strings; removing punctuation and extra spaces,
    making the text lower case and placing _ for the remaining whitespace.

    Args:
        strings (pd.Series): Panda series of strings to clean.

    Returns:
        pd.Series: Pandas series of cleaned strings.
    """
    strings = (
        strings.str.replace(r"[/]", " ", regex=True)
        .str.replace(r"[:()\%']", "", regex=True)
        .str.replace("  ", " ", regex=True)
        .str.strip()
        .str.lower()
        .str.replace(r"[^a-zA-Z0-9_]", r"_", regex=True)
        .str.replace("___", "_", regex=True)
        .str.replace("__", "_", regex=True)
    )
    return strings


def process_string(string: str) -> str:
    """Cleaning a string; removing punctuation and extra spaces,
    making the text lower case and placing _ for the remaining whitespace.

    Args:
        string (str): String to clean.

    Returns:
        str: Cleaned string.
    """
    string = (
        string.replace(r"[/]", " ")
        .replace(r"[:()\%']", "")
        .replace("  ", " ")
        .replace(" ", "_")
        .strip()
        .lower()
        .replace(r"[^a-zA-Z0-9_]", r"_")
        .replace("___", "_")
        .replace("__", "_")
    )
    return string
