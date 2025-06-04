import yaml

VALID_TEXT_EXTRACTORS = {"docling", "pdfplumber", "pymupdf", "pypdf2", "camelot"}

def load_config(config_path=None, config_dict=None):
    """
    Load the configuration for the text extraction process. This validates if necessary fields are present 
    based on the extractor settings.

    Args:
        config_path (str, optional): Path to the configuration YAML file.
        config_dict (dict, optional): Dictionary containing configuration data.

    Returns:
        dict: Validated configuration dictionary.

    Raises:
        ValueError: If the required fields are missing or invalid.
    """
    if config_path:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
    elif config_dict:
        config = config_dict
    else:
        raise ValueError("You must provide either a config_path or a config_dict.")

    # Validate the text extractor field
    if "extractor" not in config:
        raise ValueError("The 'extractor' field is required in the configuration.")
    if config["extractor"] not in VALID_TEXT_EXTRACTORS:
        raise ValueError(f"Invalid extractor specified: {config['extractor']}. Valid options are: {', '.join(VALID_TEXT_EXTRACTORS)}.")
    
    return config
