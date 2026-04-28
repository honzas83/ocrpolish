import logging
from pathlib import Path
from collections import Counter

from ocrpolish.models.metadata import LastDateSchema, MetadataSchema
from ocrpolish.services.ollama_client import OllamaClient
from ocrpolish.utils.metadata import prepend_frontmatter

logger = logging.getLogger(__name__)

# Constants for context window management
CHUNK_SIZE = 6000
LARGE_DOC_THRESHOLD = 8000

class MetadataProcessor:
    def __init__(self, ollama_client: OllamaClient, output_dir: Path, overwrite: bool = False):
        self.client = ollama_client
        self.output_dir = output_dir
        self.overwrite = overwrite
        self.tag_counts = Counter()

    def process_file(self, input_file: Path, output_file: Path, frequent_tags: list[str] | None = None) -> bool:
        """
        Processes a single file: extracts metadata and writes to output.
        """
        if output_file.exists() and not self.overwrite:
            logger.info(f"Skipping {input_file} (output already exists)")
            return False
        
        try:
            content = input_file.read_text(encoding="utf-8")
            
            # Prepare tag context if available
            tag_context = ""
            if frequent_tags:
                tag_context = (
                    f"\nIMPORTANT: Prioritize using these existing tags for consistency: {', '.join(frequent_tags)}. "
                    "Only create new tags if the current list is not sufficient."
                )
            
            # Phase 1: Primary Extraction (First chunk)
            first_chunk = content[:CHUNK_SIZE]
            prompt = (
                f"Source Filename: {input_file.name}\n\n"
                f"Document Content (First Part):\n\n{first_chunk}\n\n"
                "Please extract metadata following these strict rules:\n"
                "1. 'title' must be extracted carefully. It is usually on the first page, but could also be part of the second page (e.g., in crossposting of letters). The title should make sense in the context of the summary and abstract.\n"
                "2. 'summary' must be exactly two sentences. It must be an independent entity (define any abbreviations naturally within the text, no structural notes).\n"
                "3. 'abstract' must be a detailed overview, limited to at most 20 sentences. It must be a superset of the summary (incorporating its information) and remain an independent entity; redefine any abbreviations naturally within the text.\n"
                "4. 'mentioned_states' must only contain full names of nation states (no abbreviations).\n"
                "5. 'mentioned_organisations' should include international bodies like NATO or European Community.\n"
                "6. 'date' must be the complete official document date in ISO 8601 format (YYYY-MM-DD). Look for it on the first page.\n"
                "7. 'archive_code' should be derived using both the text and the filename provided.\n"
                "8. If the document is a letter or correspondence, strictly describe the 'sender', 'recipient', and the 'transaction' (action/purpose) imposed by the letter in the 'correspondence' field. Do not use 'N/A'; if a field is unknown, leave it empty.\n"
                "9. 'references' should contain a list of any other archive reference codes (e.g., PO/81/110, C-M(55)15) found in the document text.\n"
                "10. IMPORTANT: Convert 'author_name', 'author_institution', 'title', 'location_city', 'location_state', 'correspondence_sender', and 'correspondence_recipient' to Title Case if found in ALL CAPS. "
                "Also apply Title Case to each item in 'mentioned_states' and 'mentioned_organisations'. "
                "HOWEVER, preserve uppercase for NATO acronyms (e.g., 'NATO', 'NPG', 'DPC', 'NAC', 'SHAPE'). "
                "For example: 'NATO SECRETARY GENERAL' -> 'NATO Secretary General', 'BRUSSELS' -> 'Brussels', 'GREECE' -> 'Greece'.\n"
                "11. If 'location_city' is identified (e.g., 'Brussels'), ensure 'location_state' is filled with the corresponding nation-state (e.g., 'Belgium').\n"
                "12. Generate between 3 and 8 'tags' to interconnect documents based on specific themes, events, or topics. Tags MUST NOT contain spaces (e.g., use #NATOCommand instead of #NATO Command). Avoid generic tags like #ColdWar; instead, use tags that distinguish this document from others while still interlinking it with closely related ones.\n"
                "13. The document text is the result of OCR and may contain errors (e.g., 'CTAN' instead of 'OTAN'). Use the full context to interpret and correct these errors for the metadata extraction."
                f"{tag_context}"
            )
            
            metadata_obj = self.client.extract_structured(prompt, MetadataSchema)
            
            # Update tag counts for future consistency
            if metadata_obj.tags:
                self.tag_counts.update(metadata_obj.tags)
            
            # Convert to dict. 
            raw_dict = metadata_obj.model_dump()

            # Define order for YAML frontmatter
            ordered_keys = [
                "title", "summary", "abstract", "author_name", "author_institution"
            ]
            
            metadata_dict = {}
            # 1. Start with title, summary, abstract, and authors
            for k in ordered_keys:
                metadata_dict[k] = raw_dict.get(k, "")
            
            # 2. Insert correspondence if it exists and is valid
            corr_sender = raw_dict.get("correspondence_sender", "").strip()
            corr_recipient = raw_dict.get("correspondence_recipient", "").strip()
            corr_transaction = raw_dict.get("correspondence_transaction", "").strip()
            
            # Filter out "N/A" or effectively empty correspondence
            valid_corr = {}
            for k, v in {"sender": corr_sender, "recipient": corr_recipient, "transaction": corr_transaction}.items():
                if v and v.upper() != "N/A":
                    valid_corr[k] = v
            
            if valid_corr:
                metadata_dict["correspondence"] = valid_corr

            # 3. Add remaining primary fields
            remaining_keys = [
                "date", "archive_code", "language", "location_city", "location_state"
            ]
            for k in remaining_keys:
                metadata_dict[k] = raw_dict.get(k, "")
            
            # 4. Add collections if they have content
            for k in ["mentioned_states", "mentioned_organisations", "references", "tags"]:
                if raw_dict.get(k):
                    metadata_dict[k] = raw_dict[k]
            
            # Phase 2: Secondary Pass for Date (only if missing and document is large)
            if not metadata_dict.get("date") and len(content) > LARGE_DOC_THRESHOLD:
                logger.info(f"Date missing from first chunk of {input_file.name}. Scanning end of document...")
                last_chunk = content[-CHUNK_SIZE:]
                date_prompt = (
                    f"Document Content (Final Part):\n\n{last_chunk}\n\n"
                    "Extract ONLY the complete official date of this document if present, "
                    "in ISO 8601 format (YYYY-MM-DD)."
                )
                try:
                    date_obj = self.client.extract_structured(date_prompt, LastDateSchema)
                    if date_obj.date:
                        metadata_dict["date"] = date_obj.date
                        logger.info(f"Found date at end of document: {date_obj.date}")
                except Exception as e:
                    logger.warning(f"Secondary date extraction failed: {e}")

            # Prepend metadata to original content
            new_content = prepend_frontmatter(content, metadata_dict)
            
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(new_content, encoding="utf-8")
            return True
        except Exception as e:
            logger.error(f"Error processing {input_file}: {e}")
            return False

    def get_files(self, input_dir: Path, recursive: bool = True) -> list[Path]:
        """
        Returns a list of all .md files to be processed, excluding sidecar .filtered.md files.
        """
        pattern = "**/*.md" if recursive else "*.md"
        all_files = input_dir.glob(pattern)
        return [f for f in all_files if not f.name.endswith(".filtered.md")]

    def process_directory(self, input_dir: Path, recursive: bool = True) -> None:
        """
        Traverses directory and processes all .md files in alphabetical order.
        """
        files = sorted(self.get_files(input_dir, recursive))
        logger.info(f"Found {len(files)} markdown files in {input_dir}")
        
        for input_file in files:
            relative_path = input_file.relative_to(input_dir)
            output_file = self.output_dir / relative_path
            
            # Get 50 most frequent tags
            frequent_tags = [tag for tag, _ in self.tag_counts.most_common(50)]
            self.process_file(input_file, output_file, frequent_tags)
