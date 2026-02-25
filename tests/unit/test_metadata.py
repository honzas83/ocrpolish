from ocrpolish.utils.metadata import FileMetadataAnalyzer, PageMetadata, extract_page_number


def test_extract_page_number_format_1() -> None:
    # Pattern: - X -
    assert extract_page_number("- 5 -") == 5  # noqa: PLR2004
    assert extract_page_number("  - 123 -  ") == 123  # noqa: PLR2004
    assert extract_page_number("- 1 -") == 1

def test_extract_page_number_format_2() -> None:
    # Pattern: -X-
    assert extract_page_number("-5-") == 5  # noqa: PLR2004
    assert extract_page_number("-123-") == 123  # noqa: PLR2004
    assert extract_page_number("-1-") == 1

def test_extract_page_number_format_tilde() -> None:
    # Pattern: ~ X ~ or ~X~
    assert extract_page_number("~ 5 ~") == 5  # noqa: PLR2004
    assert extract_page_number("~123~") == 123  # noqa: PLR2004
    assert extract_page_number(" ~ 1 ~ ") == 1

def test_extract_page_number_invalid() -> None:
    assert extract_page_number("Page 5") is None
    assert extract_page_number("- X -") is None
    assert extract_page_number("123") is None
    assert extract_page_number("- 1 - some text") is None

def test_file_metadata_analyzer_threshold() -> None:
    analyzer = FileMetadataAnalyzer(threshold=0.8)
    
    # 5 pages, 4 have "HEADER", 1 has "OTHER"
    for _ in range(4):
        p = PageMetadata(header_candidates=["HEADER"], footer_candidates=["FOOTER"])
        analyzer.add_page(p)
    
    analyzer.add_page(PageMetadata(header_candidates=["OTHER"], footer_candidates=["FOOTER"]))
    
    analyzer.analyze()
    
    # HEADER: 4/5 = 80% >= 80% -> identified
    assert analyzer.identified_header == "HEADER"
    # FOOTER: 5/5 = 100% >= 80% -> identified
    assert analyzer.identified_footer == "FOOTER"

def test_file_metadata_analyzer_below_threshold() -> None:
    analyzer = FileMetadataAnalyzer(threshold=0.8)
    
    # 5 pages, 3 have "HEADER" (60%)
    for _ in range(3):
        analyzer.add_page(PageMetadata(header_candidates=["HEADER"]))
    for _ in range(2):
        analyzer.add_page(PageMetadata(header_candidates=["OTHER"]))
        
    analyzer.analyze()
    assert analyzer.identified_header is None
