import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from papyrus.core.papyrus_extractor import PapyrusExtractor
from papyrus.engine import (
    PDFPlumberExtractor,
    DoclingExtractor,
    PyMuPDFExtractor,
    PyPDF2Extractor,
    CamelotExtractor,
)

path = "./papyrus/data_pdf/invoice_100.pdf"

@pytest.mark.parametrize(
    "extractor, extractor_name, method_name, expected_capability",
    [
        (PDFPlumberExtractor(), "pdfplumber", "get_text", "text"),
        (PDFPlumberExtractor(), "pdfplumber", "get_tables", "tables"),
        (DoclingExtractor(), "docling", "get_text", "text"),
        (DoclingExtractor(), "docling","get_tables", "tables"),
        (PyMuPDFExtractor(), "pymupdf","get_text", "text"),
        (PyMuPDFExtractor(), "pymupdf", "get_tables", "tables"),
        (PyPDF2Extractor(), "pypdf2" ,"get_text", "text"),
        (CamelotExtractor(), "camelot", "get_text", "text"),     
        (CamelotExtractor(), "camelot", "get_tables", "tables"),
    ],
)

def test_extractor_method(extractor, extractor_name, method_name, expected_capability):
    config = {"extractor": extractor_name}

    papyrus_extractor = PapyrusExtractor(config_dict=config)

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


