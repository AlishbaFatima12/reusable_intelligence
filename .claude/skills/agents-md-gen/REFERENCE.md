# Advanced Patterns

## Complex FastAPI Routes

The skill handles:
- Path parameters: `/items/{item_id}`
- Query parameters (detected from function signature)
- Multiple decorators per route
- Async and sync functions

## Custom Pydantic Validators

The AST parser extracts:
- Field types (including unions: `str | None`)
- Default values
- Required vs optional fields
- Nested models (referenced by name)

## Preserving Custom Sections

To preserve custom documentation sections during regeneration, use HTML comments:

```markdown
<!-- PRESERVE START -->
## Custom Section
Your custom content here
<!-- PRESERVE END -->
```

The generator will skip overwriting content between these markers.

## Port Detection Priority

1. `.env` file: `PORT=8000` or `AGENT_NAME_PORT=8001`
2. `config.py`: `PORT = 8000` constant
3. Default: `8000`

## Handling Edge Cases

- **Empty directories**: Skipped
- **Missing FastAPI apps**: Reported as warning
- **Duplicate ports**: Flagged in validation
- **Complex routing**: Best-effort extraction with warnings
- **Missing docstrings**: Placeholder `[No description provided]`
