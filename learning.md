## Learning

### `list[str]` vs `list[list[str]]` — be concrete about what "multiple keyword sets" means
When discussing `SearchStrategy.keywords`, I explained `list[str]` as "one Vinted search call" without clarifying it already supports multiple keywords (e.g. `["linen", "trousers", "beige"]`). The user thought I was implying only one keyword per strategy. Always give a concrete example value when describing a list type to avoid ambiguity. 