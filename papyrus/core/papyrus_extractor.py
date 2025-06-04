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

from papyrus.config.config import load_config
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
        # elif model == "easyocr":
        #     extractor = EasyOCRExtractor()  
        # elif model == "tesseract":
        #     extractor = TesseractOCRExtractor() 
        # elif model == "docling-tables":
        #     extractor = TableExtractorDocling()
        # elif model == "huggingface-ocr":
        #     extractor = HuggingFaceOCRExtractor()
        
        check_capabilities(extractor, capabilities)

        return extractor
        

def check_capabilities(extractor, capabilities):
    for capability in capabilities:
        if capability not in extractor.capabilities:
            raise ValueError(f"Extractor {extractor.__class__.__name__} does not support capability '{capability}'.")
        


extractorfactory = ExtractorFactory()


class PapyrusExtractor:
    def __init__(self, config_path=None, config_dict=None):
        self.config = load_config(config_path, config_dict)
        self.extractor_factory = extractorfactory

    def get_text(self, path, format = "raw"):
        extractor = self.extractor_factory.get_processor(self.config.get("extractor"), capabilities = ['text'])
        return extractor.get_text(path, format=format)

    def get_tables(self, path):
        extractor = self.extractor_factory.get_processor(self.config.get("extractor"), capabilities = ['tables'])
        return extractor.get_tables(path)
        
    def get_all(self, path):
        extractor = self.extractor_factory.get_processor(self.config.get("extractor"), capabilities = ["text", "tables"])
        return extractor.get_tables(path)

    # @property
    # def tables(self):
    #     tables: list = []
    #     for page in self.pages.values():
    #         tables.extend(page.get("tables", []))
    #     return tables

    # def __text_by_format(self, format=""):
    #     text: str = ""
    #     for page in self.pages.values():
    #         text += page.get("text" + format, page.get("text", ""))
    #     return text

    # @property
    # def text(self, format=""):
    #     return self.__text_by_format()

    # @property
    # def text_markdown(self, format="") -> str:
    #     return self.__text_by_format(format="_md")

    # def _export_text(self, format):
    #     parts = []
    #     for p in sorted(self.pages.keys()):
    #         page = self.pages[p]
    #         if format == "md" and page.get("text_md"):
    #             parts.append(page["text_md"].strip())
    #         else:
    #             parts.append(page["text"].strip())
    #     return "\n\n".join(parts)

    # def _export_tables(self):
    #     parts = []
    #     for p in sorted(self.pages.keys()):
    #         page = self.pages[p]
    #         for i, df in enumerate(page["tables"]):
    #             parts.append(f"<!-- Page {p} - Table {i+1} -->")
    #             parts.append(df.to_markdown(index=False))
    #             parts.append("")
    #     return "\n\n".join(parts)

    # def _export_both(self):

    #     parts = []
    #     for p in sorted(self.pages.keys()):
    #         page = self.pages[p]
    #         text_content = page["text"].strip()
    #         if text_content:
    #             parts.append(text_content)
    #         for i, df in enumerate(page["tables"]):
    #             parts.append(f"<!-- Page {p} - Table {i+1} -->")
    #             parts.append(df.to_markdown(index=False))
    #         parts.append("")
    #     return "\n\n".join(parts)

    # def export(self, format="text", content="text"):

    #     assert format in {"text", "md"}, "format must be 'text' or 'md'"
    #     assert content in {
    #         "text",
    #         "tables",
    #         "both",
    #     }, "content must be 'text', 'tables', or 'both'"

    #     if content == "text":
    #         return self._export_text(format)
    #     elif content == "tables":
    #         return self._export_tables()
    #     elif content == "both":
    #         return self._export_both()

    # def extract(self, extractor: "extractor.BaseExtractor", content="text"):
    #     ExtractorFactory().get_processor(self, content, extractor)

    # def _extract_tables(self, extractor: "extractor.BaseExtractor"):
    #     for page_number in self.pages:
    #         self.pages[page_number]["tables"] = []
    #     previous_file = copy.deepcopy(self)
    #     extractor.run(self)
    #     for page_number in self.pages:
    #         if page_number in previous_file.pages:
    #             self.pages[page_number]["text"] = copy.deepcopy(
    #                 previous_file.pages[page_number].get("text", "")
    #             )
    #             self.pages[page_number]["text_md"] = copy.deepcopy(
    #                 previous_file.pages[page_number].get("text_md", "")
    #             )
    #         else:
    #             self.pages[page_number]["text"] = ""
    #             self.pages[page_number]["text_md"] = ""

    #     return self

    # def _extract_text(self, extractor: "extractor.BaseExtractor"):
    #     for page_number in self.pages:
    #         self.pages[page_number]["text"] = ""
    #         self.pages[page_number]["text_md"] = ""
    #     previous_file = copy.deepcopy(self)
    #     extractor.run(self)
    #     for page_number in self.pages:
    #         if page_number in previous_file.pages:
    #             self.pages[page_number]["tables"] = copy.deepcopy(
    #                 previous_file.pages[page_number].get("tables", [])
    #             )
    #         else:
    #             self.pages[page_number]["tables"] = []

    #     return self

    # def _extract_all(self, extractor: "extractor.BaseExtractor"):
    #     extractor.run(self)
    #     return self

    # def show_capabilities(self, extractor: "extractor.BaseExtractor"):
    #     caps = getattr(extractor, "capabilities", set())
    #     print(
    #         f"{extractor.__class__.__name__} supports: {', '.join(caps) or 'nothing'}"
    #     )
