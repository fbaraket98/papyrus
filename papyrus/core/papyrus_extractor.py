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

from typing import List

from papyrus.config.config import check_config
from papyrus.engine.extractor import (
    DoclingExtractor,
    PDFPlumberExtractor,
    PyMuPDFExtractor,
    PyPDF2Extractor,
    CamelotExtractor
)

class ExtractorFactory:
    @staticmethod
    def get_processor(model: str, capabilities: List[str]):
        """
        Factory method to return the appropriate text extractor or OCR processor based on the model.

        Args:
            model (str): The model name to select the extractor (e.g., "docling", "pdfplumber", "pymupdf", "pypdf2", "easyocr", "tesseract").

        Returns:
            BaseTextExtractor or BaseOCRExtractor: The appropriate extractor instance.

        Raises:
            ValueError: If the specified model is not recognized.
        """
        if model == "docling":
            extractor = DoclingExtractor()
        elif model == "pdfplumber":
            extractor = PDFPlumberExtractor()
        elif model == "pymupdf":
            extractor = PyMuPDFExtractor()
        elif model == "pypdf2":
            extractor = PyPDF2Extractor()
        elif model == "camelot":
            extractor = CamelotExtractor()
        
        check_capabilities(extractor, capabilities)

        return extractor
        

def check_capabilities(extractor, capabilities):
    for capability in capabilities:
        if capability not in extractor.capabilities:
            raise ValueError(f"Extractor {extractor.__class__.__name__} does not support capability '{capability}'.")
        


extractorfactory = ExtractorFactory()


class PapyrusExtractor:
    def __init__(self, extractor=None):
        self.extractor = extractor
        check_config(extractor)
        self.extractor_factory = extractorfactory

    def get_text(self, path, format = "raw",correct=False)->str:
        extractor = self.extractor_factory.get_processor(self.extractor, capabilities = ['text'])
        if correct :
            from papyrus.tools import speling_correction
            text = extractor.get_text(path, format=format)
            text = speling_correction.correct_spelling_text(text)
            return text
        else:
            return extractor.get_text(path, format=format)

    def get_tables(self, path, correct=False)->List:
        extractor = self.extractor_factory.get_processor(self.extractor, capabilities = ['tables'])
        if correct:
            from papyrus.tools import speling_correction
            tables = extractor.get_tables(path)
            tables = speling_correction.correct_spelling_tables(tables)
            return tables
        else:
            return extractor.get_tables(path)
        
    def get_all(self, path):
        extractor = self.extractor_factory.get_processor(self.extractor, capabilities = ["text", "tables"])
        return extractor.get_tables(path)
