from typing import Dict, List, Any

SYSTEM_PROMPT_STATUS = (
    "You are an IT operations communications assistant. "
    "Write clear, factual updates with no hallucinations. "
    "If data is missing, say it's missing."
)

def build_progress_prompt(change_id: str, stats: Dict[str, Any], failures: List[Dict[str, Any]]) -> str:
    return f"""
We are running monthly Linux patching for change: {change_id}

Stats (from automation DB):
{stats}

Failures (top items):
{failures}

Task:
1) Create a short stakeholder update (non-technical, 5-8 lines).
2) Create a patching-team update (technical bullets) that lists:
   - which stage is failing most
   - top suspected causes based on summaries
   - recommended next actions (safe + practical)
Output plain text only.
""".strip()
