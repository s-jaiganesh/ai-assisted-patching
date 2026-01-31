def build_progress_prompt(change_id: str, stats: dict, failures: list) -> str:
    return f"""You are an SRE assistant helping communicate a Linux monthly patching window.

Change: {change_id}

Using the stats + failures below, produce TWO sections:
A) Stakeholder Update (non-technical, 4-6 lines)
B) Patching Team Update (more technical, bullet list + next actions)

Be concise.

STATS:
{stats}

FAILURES (up to 20 hosts):
{failures}
"""
