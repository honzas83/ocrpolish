# Quickstart: Tag Grouping Prefixes (Updated v2)

This guide explains how to verify the new three-tiered tag grouping and how to disable prefixes.

## Verification Steps

1. **Process a Document**:
   ```bash
   ocrpolish metadata <input_dir> <output_dir>
   ```

2. **Verify Tag Groups**:
   - **Topics**: Should appear as `- #Topics/...`
   - **Entities**: Should appear as `  - #Entities/...`
   - **Tags**: Should appear as `#Tags/...`

## Disabling a Prefix Group

To remove a root category (e.g., you don't want the `#Entities/` prefix):
1. Open `ocrpolish/data_model.py`.
2. Set the relevant constant to `None`:
   ```python
   TAG_PREFIX_ENTITY: str | None = None
   ```
3. Re-run processing. All entity tags will now appear as `#State/...` or `#Org/...` without the top-level `Entities/` root.

## Changing Prefix Values

To rename a root category (e.g., back to singular):
1. Open `ocrpolish/data_model.py`.
2. Change the value:
   ```python
   TAG_PREFIX_TOPIC: str | None = "Topic"
   ```
3. Re-run processing.
