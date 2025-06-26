from sympy import content

# papyrus
This library aims at extracting text and tables from pdf.

### Installation
You can install the library with
``` powershell
python -m pip install https://github.com/eurobios-mews-labs/papyrus.git
```

## Basic usage
1. Choose you extractor from engine.py
- engine.PDFPlumberExtractor()
- engine.DoclingExtractor()
- engine.PyMuPDFExtractor()
- engine.PyPDF2Extractor() 
- engine.EasyOCRExtractor()
- engine.TesseractOCRExtractor() 
- engine.HuggingFaceOCRExtractor() 
- engine.CamelotExtractor()

| Extractor               | extracting text | extract tables |
|:------------------------|:---------------:|---------------:|
| PDFPlumber              |        X        |              X |
| Docling                 |        X        |              X |
| PyMuPDFExtractor        |        X        |                |
| PyPDF2Extractor         |        X        |                |
| CamelotExtractor        |        X        |              X |
  
2. Depending on the extractor chosen you can extract only text or only table or both.

````python
from papyrus import engine
from papyrus.core import File

file_path = "invoice_100.pdf"
#Choose the pdf_plumber extractor 
pdf_plumber = engine.PDFPlumberExtractor()
# instanciate File with the file_path 
file = File(file_path)
#extract only text
file.extract(content="text", extractor=pdf_plumber)
#print the result
print(file.text)
#extract only tables
file.extract(content="tables",extractor=pdf_plumber)
print(file.tables)
#extract both text and tables
file.extract(content="all", extractor=pdf_plumber)
````

## Contributing

You are very welcome to contribute to the project, by requesting features,
pointing out new tools that can be added as component, by identifying issues and creating new features. 
Development guidelines will be detailed in near future.

* Fork the repository
* Clone your forked repository ```git clone https://github.com/$USER/papyrus.git```
* Test using pytest ````pip install pytest; pytest tests/````
* Submit you work with a pull request.