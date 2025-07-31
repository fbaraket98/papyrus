import re
import pandas as pd
import Levenshtein



def load_df_spellcheck()->pd.DataFrame:
    """
    Loads the dataframe used to make the spelling correction, and sort the entries by
    number of usage according to Google statistics, from highest to lowest.
    """
    df = pd.read_csv( "./papyrus/tools/words_dict/linux_dict_cleaned.csv")
    df["length"] = df["word"].str.len()
    df = df.sort_values(by=["length", "count"], ascending=[True, False]).reset_index(drop=True)
    return df


df_spellcheck = load_df_spellcheck()

MAX_LEN_SPELLCHECK = df_spellcheck["word"].str.len().max()  # longer word in df_spellcheck
SET_SPELLCHECK_WORDS = set(df_spellcheck["word"])  # set of words in df_spellcheck


def l_for_i(text: str) -> str:
    """
    With OCR, i can be mistaken for l. This function checks impossible english patterns, such as three consecutive
    consonants including a l that would indicate that the l is likely an i. eg: alrbus instead of airbus
    Possible series of consonnants: spl (split), sql, lkt, lks (silks), lfs (gulfs), lpt (helpt), lps (helps) and those
    with a double consonnant + l (bottle, supple, battle) and some others with ly such as awkwardly.
    Capital letters are not corrected to not alter acronyms.
    """
    pat1 = r"(?:(?<=[b-df-hjkmnp-tv-z]{2})(?<!sp))l(?![ey])"
    pat2 = r"l(?:(?=[b-df-hjkmnp-tv-z]{2})(?!ks)(?!fs)(?!kt)(?!pt)(?!ps))"
    pat3 = r"(?<=[b-df-hjkmnp-tv-z])l(?=[b-df-hjkmnp-tv-xz])"
    pattern = rf"({pat1}|{pat2}|{pat3})"
    text = re.sub(pattern, "i", text)
    return text


def o_for_0(text: str) -> str:
    """
    With OCR, o can be mistaken for 0. This function ensures that o's directly following numbers are
    replaced by 0. The replacement is iterative. o is replaced by a 0, then if what follows the new 0
    is also a o, it is replaced by a 0, ... until 6 times to account for numbers in the order of million.
    """
    counter = 0
    one_more_pass = True
    pat1 = r"(?:(?<=\d)|(?<=\d\.)|(?<=\d,)|(?<=\d'))(o|O)"
    pat2 = r"(o|O)(?=\d(\.|,|')?)"
    pattern = rf"({pat1}|{pat2})"
    while counter < 6 and one_more_pass:
        one_more_pass = False
        counter += 1
        new_text = re.sub(pattern, "0", text)
        if id(new_text) != id(text):
            one_more_pass = True
            text = new_text
    return text


def words_correction(text: str, use_hamming: bool = False) -> str:
    """
    The correction relies on the hamming distance, correcting words only with the best found match in the
    dictionary that has the same length than the initial word.

    :param text: the text that should be corrected
    :param use_hamming: boolean. If true, uses the hamming distance for faster computation.
    However, hamming only corrects with a word of the same length, thus not accounting for deletion or insertion.
    If False, uses'levenshtein', a slower method but that can makes correction with up to 1 deletion or insertion.
    """
    # split text into words and create a pandas series with the words to apply the corrections
    text_words = pd.Series(re.split(r"((?<=\b)|(?<=\n)[a-z]+(?:\b))", text))
    # exclude words with capital letter (they could be acronyms or proper nouns that are not in the spelling dictionnary)
    # exclude short words (the risk to correct them wrong is too high)
    # exclude long words (could be a code or technical words, that should not or cannot be corrected)
    # exclude words found in the dictionary (they do not need to be corrected)
    mask = (text_words.str.contains(r"\d|[A-Z]{1}|\W", regex=True)) | (text_words.str.len() < 5) | (
                text_words.str.len() > MAX_LEN_SPELLCHECK) | text_words.isin(SET_SPELLCHECK_WORDS)
    dict_correct = {}  # dictionnary of words to correct. key: wrong spelling found in text, value: correction
    for word in text_words.loc[~mask].unique():
        lower_word = word.lower()
        if use_hamming:
            candidates = df_spellcheck.query(f"length == {len(lower_word)}")["word"]
        else:
            candidates = \
            df_spellcheck.query(f"length in [{len(lower_word) - 1}, {len(lower_word)}, {len(lower_word) + 1}]")["word"]
        if len(candidates) > 0:
            if use_hamming:
                distance = candidates.apply(lambda x: Levenshtein.hamming(lower_word, x))
            else:
                distance = candidates.apply(
                    lambda x: Levenshtein.distance(lower_word, x, weights=(3, 3, 2), score_cutoff=5))
            idx_min = int(distance.idxmin())
            if distance[idx_min] == 1:
                dict_correct[word] = candidates.loc[idx_min]
    # apply the corrections
    mask = text_words.isin(dict_correct.keys())
    text_words.loc[mask] = text_words.loc[mask].apply(lambda x: dict_correct[x])
    # transform back into a text and return result
    return "".join(text_words)

def correct_spelling_text(text)->str:
    text = l_for_i(text)
    text = o_for_0(text)
    text = words_correction(text, use_hamming=True)
    return text

def correct_spelling_tables(tables)->list:
    corrected_tables = []
    for table in tables:
        table = table.rename(columns=lambda col: correct_spelling_text(col))
        table = table.map(correct_spelling_text)
        corrected_tables.append(table)
    return corrected_tables

