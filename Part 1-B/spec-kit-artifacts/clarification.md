# Clarification

## Interpretation
- “AI-assisted” is implemented as a deterministic source-analysis agent rather
  than a network call, making evaluation repeatable.
- The initial supported language is Python.
- Findings are evidence-based pattern observations; no external model is required.
- An evaluation case may specify `no_findings: true` for a clean-source edge case.
- Semantic evaluation rewards category, severity, line, finding keywords, and
  suggestion keywords.

## Assumptions
- Source is provided as text and source line numbering starts at 1.
- Syntax may be incomplete in a review snippet.
- Empty output is valid for source with no detected pattern.

## Out of scope
- Full IDE integration
- Automatic source rewriting
- Remote model providers
- Cross-language parsing beyond the Python implementation in this project
