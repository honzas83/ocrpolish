import re
import textwrap

from ocrpolish.data_model import ProcessingConfig


def should_protect_line(line: str, protected_prefixes: list[str]) -> bool:
    """Check if a line starts with a protected markdown prefix."""
    trimmed = line.lstrip()
    # Also protect standard document structures like ANNEX or APPENDIX
    extra_protected = ["ANNEX", "APPENDIX"]
    if any(trimmed.upper().startswith(p) for p in extra_protected):
        return True
    return any(trimmed.startswith(p) for p in protected_prefixes)


def is_structural_marker(line: str) -> bool:
    """Check if a line matches a structural pattern that MUST be preserved."""
    patterns = [
        r"^#\s*Page\s+\d+$",  # # Page 3
        r"^\d+-\d+$",  # 1-1
        r"^Page\s+\d+$",  # Page 3
        r"^\d+$",  # 3
    ]
    return any(re.match(p, line.strip(), re.IGNORECASE) for p in patterns)


def is_noisy_boilerplate(line: str) -> bool:
    """Check if a line matches known variable boilerplate that SHOULD be removed."""
    patterns = [
        r"DECLASSIFIED",
        r"PUBLICLY DISCLOSED",
        r"MISE EN LECTURE PUBLIQUE",
        r"DECLASSIFI[EÉ]",
    ]
    stripped = line.strip().upper()
    return any(re.search(p, stripped) for p in patterns)


def wrap_lines(lines: list[str], config: ProcessingConfig) -> list[str]:
    """Wrap long lines while respecting protected prefixes and typewriter width."""
    processed_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        raw_line = line.rstrip("\n")

        if not stripped:
            # Preserve blank lines
            if processed_lines and processed_lines[-1] != "":
                processed_lines.append("")
        elif should_protect_line(line, config.protected_prefixes):
            # Bypass wrapping for protected elements
            processed_lines.append(line.rstrip())
        elif len(raw_line) > config.typewriter_width:
            # Wrap long lines (flush left for subsequent lines)
            wrapped = textwrap.wrap(
                stripped, width=config.typewriter_width, subsequent_indent=""
            )
            processed_lines.extend(wrapped)
        else:
            # Preserve shorter lines as they are
            processed_lines.append(stripped)

    return processed_lines


def clean_lines(lines: list[str], global_headers: set[str], config: ProcessingConfig) -> list[str]:
    """Perform header/footer removal and paragraph wrapping."""
    # First pass: Filter out headers/footers
    filtered_lines = []
    for line in lines:
        stripped = line.strip()
        
        # 1. Always preserve structural markers
        if is_structural_marker(stripped):
            filtered_lines.append(line)
            continue
            
        # 2. Always remove noisy variable boilerplate
        if is_noisy_boilerplate(stripped):
            continue
            
        # 3. Remove statistical headers/footers
        if stripped in global_headers:
            continue
            
        filtered_lines.append(line)

    if not filtered_lines:
        return []

    processed_lines = wrap_lines(filtered_lines, config)

    # Final cleanup: ensure exactly one empty line between paragraphs
    final_output: list[str] = []
    for line in processed_lines:
        if not line:
            if final_output and final_output[-1] != "":
                final_output.append("")
        else:
            final_output.append(line)

    return final_output
