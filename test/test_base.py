import pandas as pd
import pytest

from papyrus import engine
from papyrus.core.file import File


path = "invoice_100.pdf"
extractor_list = [
        engine.PDFPlumberExtractor(),
        # engine.DoclingExtractor(),
        # engine.PyMuPDFExtractor(),
        # engine.PyPDF2Extractor(),
        # engine.EasyOCRExtractor(),
        # engine.TesseractOCRExtractor(),
        # engine.HuggingFaceOCRExtractor(),
        # engine.CamelotExtractor(),
    ]


def run_extractor_content_text_only(extractor, file: File = File(path)):
    """
    Test extraction "text" only
    At default, it must contain all texts found & no table returned

    """
    file.extract(content="text", extractor=extractor)
    assert isinstance(file.text, str), "file.text must be typed as text"
    assert isinstance(file.tables, list) & (len(file.tables) == 0), "file.tables should be empty when context='text'"


def run_extractor_content_table_only(extractor, file: File = File(path)):
    """
    Test extraction "table" only
    At default, it must contain all tables found & no text returned

    """
    file.extract(content="table", extractor=extractor)
    assert isinstance(file.tables, list), "file.tables must be typed as list"
    # if tables are not empty, it's elements must be typed as pandas dataframe
    if file.tables:
        assert (all(isinstance(df, pd.DataFrame) for df in file.tables)), "Not all items are pandas DataFrames"

    assert isinstance(file.text, str) & (len(file.text) == 0), "file.text should be empty when context='table'"


def run_extractor_content_all(extractor, file: File = File(path)):
    """
    Test extraction "all"
    At default, it must return all texts & tables found
    """

    file.extract(content="all", extractor=extractor)
    assert isinstance(file.text, str), "file.text must be typed as text"
    assert isinstance(file.tables, list), "file.tables must be typed as list"
    # if tables are not empty, it's elements must be typed as pandas dataframe
    if file.tables:
        assert (all(isinstance(df, pd.DataFrame) for df in file.tables)), "Not all items are pandas DataFrames"


@pytest.mark.parametrize("extractor", extractor_list)
def test_all_extractors_content_text_only(extractor):
    print(f"\nTesting with content = 'text' for extractor: {extractor.__class__}")
    run_extractor_content_text_only(extractor)


@pytest.mark.parametrize("extractor", extractor_list)
def test_all_extractors_content_table_only(extractor):
    print(f"\nTesting with content = 'table' for extractor: {extractor.__class__}")
    run_extractor_content_table_only(extractor)


@pytest.mark.parametrize("extractor", extractor_list)
def test_all_extractors_content_all(extractor):
    print(f"\nTesting with content = 'all' for extractor: {extractor.__class__}")
    run_extractor_content_all(extractor)
