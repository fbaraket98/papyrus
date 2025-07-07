import pytest

from papyrus.core.papyrus_extractor import PapyrusExtractor
from papyrus.engine import (
    PDFPlumberExtractor,
    DoclingExtractor,
    PyMuPDFExtractor,
    PyPDF2Extractor,
    CamelotExtractor,
)

path = "invoice_100.pdf"


@pytest.mark.parametrize(
    "extractor, extractor_name, method_name, expected_capability",
    [
        (PDFPlumberExtractor(), "pdfplumber", "get_text", "text"),
        (PDFPlumberExtractor(), "pdfplumber", "get_tables", "tables"),
        (DoclingExtractor(), "docling", "get_text", "text"),
        (DoclingExtractor(), "docling", "get_tables", "tables"),
        (PyMuPDFExtractor(), "pymupdf", "get_text", "text"),
        (PyMuPDFExtractor(), "pymupdf", "get_tables", "tables"),
        (PyPDF2Extractor(), "pypdf2", "get_text", "text"),
        (CamelotExtractor(), "camelot", "get_text", "text"),
        (CamelotExtractor(), "camelot", "get_tables", "tables"),
    ],
)
def test_extractor_method(extractor, extractor_name, method_name, expected_capability):
    print(f"{extractor_name}==" )
    papyrus_extractor = PapyrusExtractor(extractor=extractor_name)

    capabilities = getattr(extractor, "capabilities", set())

    if expected_capability in capabilities:
        method = getattr(papyrus_extractor, method_name)
        result = method(path)
        if method_name == "get_tables":
            assert isinstance(result, list)
        else:
            assert isinstance(result, str)
    else:
        with pytest.raises(Exception):
            method = getattr(papyrus_extractor, method_name)
            method(path)


@pytest.mark.parametrize(
    "extractor_name",
    [
        ("pdfplumber"),
        ("docling"),
        ("pymupdf"),
        ("pypdf2"),
    ],
)
def run_extractor_content_text_only(extractor_name):
    """
    Test extraction "text" only
    At default, it must contain all texts found 

    """
    papyrus_extractor = PapyrusExtractor(extractor=extractor_name)
    text = papyrus_extractor.get_text(path)
    assert isinstance(text, str), "text must be typed as str"


@pytest.mark.parametrize(
    "extractor_name",
    [
        ("pdfplumber"),
        ("docling"),
        ("pymupdf"),
        ("camelot"),
    ],
)
def run_extractor_content_tables_only(extractor_name):
    """
    Test extraction "tables" only
    At default, it must contain all tables found

    """
    papyrus_extractor = PapyrusExtractor(extractor=extractor_name)
    tables = papyrus_extractor.get_tables(path)
    assert isinstance(tables, list), "tables must be typed as list"


@pytest.mark.parametrize(
    "extractor_name",
    [
        ("pdfplumber"),
        ("docling"),
        ("pymupdf"),
        ("pypdf2"),
    ],
)
def run_extractor_content_all(extractor_name):
    """
    Test extraction "all" 
    At default, it must contain all texts and tables found 

    """
    papyrus_extractor = PapyrusExtractor(extractor=extractor_name)
    text = papyrus_extractor.get_all(path)
    assert isinstance(text, str), "text must be typed as str"
