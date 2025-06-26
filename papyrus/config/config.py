VALID_TEXT_EXTRACTORS = {"docling", "pdfplumber", "pymupdf", "pypdf2", "camelot"}

def check_config(extractor):
    """
    check_config validates the configuration for the text extractor.
    It ensures that the extractor is a valid string and that it matches one of the predefined extractors.s

    Args:
        extractor (str): The type of text extractor to use. Must be one of the valid extractors.
        Valid options are: 'docling', 'pdfplumber', 'pymupdf', 'pypdf2', 'camelot'.

    Raises:
        ValueError: If the required fields are missing or invalid.
    """

    if not isinstance(extractor, str):
        raise ValueError("The 'extractor' field must be a string representing the extractor type.")

    if extractor is None:
        raise ValueError("The 'extractor' field is required in the configuration.")
    if extractor not in VALID_TEXT_EXTRACTORS:
        raise ValueError(f"Invalid extractor specified: {extractor}. Valid options are: {', '.join(VALID_TEXT_EXTRACTORS)}.")

