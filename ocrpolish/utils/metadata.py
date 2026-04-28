import re
from collections import Counter
from typing import Any

import yaml

from ocrpolish.data_model import PageMetadata


def parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """
    Parses YAML frontmatter from a string.
    Only consumes the frontmatter if it is a valid YAML dictionary.
    
    Args:
        content: The content of the file.
        
    Returns:
        A tuple containing (metadata_dict, body_content).
    """
    if not content.startswith("---"):
        return {}, content
    
    # Split by lines that are exactly '---'
    parts = re.split(r"^---\s*$", content, maxsplit=2, flags=re.MULTILINE)
    
    if len(parts) < 3:
        # Not a complete frontmatter block
        return {}, content
    
    try:
        metadata = yaml.safe_load(parts[1])
        if isinstance(metadata, dict):
            return metadata, parts[2].lstrip()
    except yaml.YAMLError:
        pass
        
    # If not a dict or failed to parse, it's just content that happens to have ---
    return {}, content


def stringify_frontmatter(metadata: dict[str, Any]) -> str:
    """
    Converts a dictionary to a YAML frontmatter string.
    """
    if not metadata:
        return ""
    
    yaml_str = yaml.safe_dump(metadata, sort_keys=False, allow_unicode=True)
    return f"---\n{yaml_str}---\n"


def prepend_frontmatter(content: str, metadata: dict[str, Any]) -> str:
    """
    Prepends metadata as YAML frontmatter to content, merging with existing if present.
    Follows strict rules to avoid double delimiters and preserve document structure.
    """
    existing_metadata, body = parse_frontmatter(content)
    merged_metadata = {**existing_metadata, **metadata}
    
    if not merged_metadata:
        return content
    
    yaml_str = yaml.safe_dump(merged_metadata, sort_keys=False, allow_unicode=True)
    
    # User instruction: "Just check if the original MD starts with '---' (it should) 
    # and do not add additional '---' after the frontmatter."
    if body.startswith("---"):
        # Original file already has a delimiter we can use as the closing one.
        # We prepend our opening delimiter and the YAML.
        return f"---\n{yaml_str}{body}"
    else:
        # File doesn't start with ---, so we provide both delimiters.
        return f"---\n{yaml_str}---\n{body.lstrip()}"


class FileMetadataAnalyzer:
    """Analyzes metadata patterns across all pages of a single file."""

    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold

    def analyze(self, pages: list[PageMetadata]) -> set[frozenset[str]]:
        """Identify boilerplate patterns across multiple pages."""
        pattern_counts = Counter()
        total_pages = len(pages)

        for page in pages:
            # Check headers and footers
            patterns = set()
            patterns.update(page.header_left)
            patterns.update(page.header_right)
            patterns.update(page.footer_left)
            patterns.update(page.footer_right)

            for p in patterns:
                pattern_counts[p] += 1

        # Keep patterns that appear in more than threshold% of pages
        threshold_count = total_pages * self.threshold
        frequent_patterns = {
            frozenset([p]) for p, count in pattern_counts.items() if count >= threshold_count
        }

        return frequent_patterns


def extract_page_number(line: str) -> int | None:
    """Extract page number from a line like '- 5 -' or '~ 5 ~'."""
    match = re.search(r"[-~]\s*(\d+)\s*[-~]", line)
    if match:
        return int(match.group(1))
    return None
