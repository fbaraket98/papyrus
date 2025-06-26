# Copyright 2025 Mews Labs
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import copy
from abc import ABC, abstractmethod
from typing import Optional


from papyrus.tools.text_processing import text_without_tables


class BaseExtractor(ABC):
    """
    Abstract base class for all text extractors.
    All concrete extractors must implement the `get_text`, `get_tables`, and `get_all` methods.
    Each extractor can have specific capabilities, which are defined in the `capabilities` attribute.
    """

    def __init__(self, capabilities=set()) -> None:
        self.capabilities = set()
        if not isinstance(self, BaseExtractor):
            raise TypeError(
                f"Expected extractor to be an instance of BaseExtractor, got {type(self).__name__} instead."
            )

    @abstractmethod
    def get_text(self, path: str, **kwargs):
        pass

    @abstractmethod
    def get_tables(self, path: str, **kwargs):
        pass

    @abstractmethod
    def get_all(self, path: str, **kwargs):
        pass


class DoclingExtractor(BaseExtractor):
    def __init__(self):
        super().__init__()
        self.capabilities = {"text", "tables", "text_ocr", "tables_orc"}

    def get_text(self, path: str, **kwargs):
        format = kwargs.get("format", "raw")
        try:
            from docling.document_converter import DocumentConverter
        except ImportError:
            raise ImportError("'docling' is not installed. Run `pip install docling`")

        doc_converter = DocumentConverter()
        conv_res = doc_converter.convert(path)
        if format == "raw":
            page_text = conv_res.document.export_to_text()
        elif format == "markdown":
            page_text = conv_res.document.export_to_markdown()
        return page_text

    def get_tables(self, path: str):
        try:
            from docling.document_converter import DocumentConverter
        except ImportError:
            raise ImportError("'docling' is not installed. Run `pip install docling`")
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("'pandas' is not installed. Run `pip install pandas`")

        doc_converter = DocumentConverter()
        conv_res = doc_converter.convert(path)
        tables = []
        for table in conv_res.document.tables:
            table_df: pd.DataFrame = table.export_to_dataframe()
            tables.append(table_df)
        return tables
    
    def get_all(self, path: str, **kwargs):
        format = kwargs.get("format", "raw")
        try:
            from docling.document_converter import DocumentConverter
        except ImportError:
            raise ImportError("'docling' is not installed. Run `pip install docling`")
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("'pandas' is not installed. Run `pip install pandas`")
        
        doc_converter = DocumentConverter()
        conv_res = doc_converter.convert(path)
        if format == "raw":
            text = conv_res.document.export_to_text() + "\n\n"
        elif format == "markdown":  
            text = conv_res.document.export_to_markdown() + "\n\n"
        for table in conv_res.document.tables:
            table_df: pd.DataFrame = table.export_to_dataframe()
            text += table_df.to_markdown() + "\n\n"
        return text
    

class PDFPlumberExtractor(BaseExtractor):
    def __init__(self):
        super().__init__()
        self.capabilities = {"text", "tables"}

    def get_text(self, path: str, **kwargs):
        try:
            import pdfplumber
        except ImportError:
            raise ImportError("'pdfplumber' is not installed. Run `pip install pdfplumber`")

        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = text_without_tables(page) or ""
                text += page_text.strip() + "\n\n"
        return text

    def get_tables(self, path: str, **kwargs):
        try:
            import pdfplumber
        except ImportError:
            raise ImportError("'pdfplumber' is not installed. Run `pip install pdfplumber`")
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("'pandas' is not installed. Run `pip install pandas`")

        tables = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                table_data = page.extract_table()
                if table_data:
                    df = pd.DataFrame(table_data)
                    if not df.empty:
                        tables.append(df)
        return tables

    def get_all(self, path: str, **kwargs):
        try:
            import pdfplumber
            import pandas as pd
        except ImportError:
            raise ImportError("Required packages not installed. Run `pip install pdfplumber pandas`")

        full_text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = text_without_tables(page) or ""
                full_text += page_text.strip() + "\n\n"
                table_data = page.extract_table()
                if table_data:
                    df = pd.DataFrame(table_data)
                    if not df.empty:
                        full_text += df.to_markdown() + "\n\n"
        return full_text

class PyMuPDFExtractor(BaseExtractor):
    def __init__(self, capabilities=set()):
        super().__init__()
        self.capabilities = {"text", "tables"}
        self.output = None

    def get_text(self, path: str, **kwargs):
        try:
            import fitz
        except ImportError:
            raise ImportError("'PyMuPDF' is not installed. Run `pip install pymupdf`")

        text = ""
        doc = fitz.open(path)
        for page in doc:
            page_text = page.get_text()
            text += page_text.strip() + "\n\n"
        return text

    def get_tables(self, path: str, **kwargs):
        
        try:
            import fitz
            import pandas as pd
        except ImportError:
            raise ImportError("Required packages not installed. Run `pip install pymupdf pandas`")

        tables = []
        doc = fitz.open(path)
        for page in doc:
            for table in page.find_tables():
                df = table.to_pandas()
                if not df.empty:
                    tables.append(df)
        return tables

    def get_all(self, path: str, **kwargs):
        try:
            import fitz
            import pandas as pd
        except ImportError:
            raise ImportError("Required packages not installed. Run `pip install pymupdf pandas`")

        text = ""
        doc = fitz.open(path)
        for page in doc:
            page_text = page.get_text()
            text += page_text.strip() + "\n\n"
            for table in page.find_tables():
                df = table.to_pandas()
                if not df.empty:
                    text += df.to_markdown() + "\n\n"
        return text


class PyPDF2Extractor(BaseExtractor):
    def __init__(self):
        super().__init__()
        self.capabilities = {"text"}

    def get_text(self, path: str, **kwargs):
        try:
            import PyPDF2
        except ImportError:
            raise ImportError("'PyPDF2' is not installed. Run `pip install PyPDF2`")

        text = ""
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text() or ""
                text += page_text.strip() + "\n\n"
        return text

    def get_tables(self, path: str, **kwargs):
        pass
    def get_all(self, path: str, **kwargs):
        pass

class CamelotExtractor(BaseExtractor):
    def __init__(self, capabilities=set()):
        super().__init__()
        self.capabilities = {"tables"}

    def get_tables(self, path: str, **kwargs):
        try:
            import camelot
        except ImportError:
            raise ImportError("'camelot' is not installed. Run `pip install camelot`")

        tables_out = camelot.read_pdf(path, pages="all", flavor="stream")
        tables = [table.df for table in tables_out if not table.df.empty]

        return tables

    def get_text(self, path: str, **kwargs):
        pass

    def get_all(self, path: str):
        pass

