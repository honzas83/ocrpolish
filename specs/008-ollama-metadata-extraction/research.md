# Research: Ollama Metadata Extraction

## Decision: Ollama Structured Output with Pydantic
**Rationale**: Ollama (v0.5.0+) supports native grammar-constrained decoding. By passing a Pydantic model's JSON schema to the `format` parameter, we ensure the model *must* return valid JSON that conforms to our metadata structure.
**Alternatives considered**: 
- **Plain Prompting**: Unreliable, often requires complex regex or multiple retries to get valid JSON.
- **Instructor Library**: Excellent but adds another dependency. Ollama's native support is sufficient for our current needs.

## Decision: Context Management Strategy
**Rationale**: Gemma 2 26B has an 8k context window. Most metadata (author, title, archive code) resides in the first few pages. We will prioritize the first 6,000 tokens for primary extraction. To handle `last_date` across the entire document, we will:
1. Extract primary metadata from the first chunk.
2. If document > 6k tokens, perform a quick scan of the final chunk specifically for dates to identify the `last_date`.
**Alternatives considered**:
- **Full Document Map-Reduce**: Overkill for basic metadata and too slow/expensive for local LLMs.
- **RAG**: Adds complexity (vector DB) that isn't justified for this specific metadata set.

## Decision: YAML Frontmatter Handling
**Rationale**: We will use a custom utility function utilizing `pyyaml` for prepending metadata. This avoids adding the `python-frontmatter` dependency while providing full control over the `---` delimiters and ensuring `utf-8` encoding.
**Alternatives considered**:
- **python-frontmatter**: A robust choice, but the manual approach is simpler to integrate into our existing `files.py` utilities.

## Decision: Model Selection
**Rationale**: The user explicitly requested `gemma4:26b`. We will make this configurable via CLI but default to this model.
**Alternatives considered**:
- **Llama 3.1 8B**: Faster, but the user specifically targeted Gemma for its reasoning capabilities in this domain.
