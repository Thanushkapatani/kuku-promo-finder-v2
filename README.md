# Kuku Promo Finder — Version 2

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```
Upload the provided ZIP containing episode TXT files.

## What changed in V2
- Reads screenplay section labels to distinguish dialogue, action and camera beats.
- Prefers actual dialogue for opening and ending beats, but labels visual/action fallbacks honestly.
- Uses episode loglines as lightweight context.
- Aligns candidate starts to timestamped beat starts.
- Suppresses candidates with >=25% overlap relative to the shorter segment.
- Exports ranked CSV and JSON.

## Scoring
The transparent heuristic gives bonuses for dialogue at the opening and ending, counts a bounded set of tension terms, adds beat-density credit and small logline-overlap credit. This is a triage baseline, not an LLM or a measure of audience performance. Editors must review standalone clarity, visual continuity, and whether the ending is genuinely unresolved.

## Known limitations
Keyword signals are context-insensitive; the tool does not understand sarcasm, visual performance, cross-episode context, or rights/editing constraints. Logline overlap is a weak proxy for standalone clarity. Dialogue may not always be the strongest hook. No external LLM/API is called.
