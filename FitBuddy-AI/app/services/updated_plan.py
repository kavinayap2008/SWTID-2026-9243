from ..config import get_settings
from .gemini_client import generate_text


def update_workout_plan(
    original_plan: str,
    feedback: str,
) -> str:

    settings = get_settings()

    # -----------------------------------------------------
    # MOCK MODE
    # -----------------------------------------------------

    if settings.mock_ai:

        return (
            original_plan
            + "\n\n"
            + "Requested adjustment applied:\n"
            + feedback
            + "\n\n"
            + "The requested change should be incorporated "
              "while preserving appropriate recovery and "
              "safe progression."
        )

    # -----------------------------------------------------
    # GEMINI UPDATE PROMPT
    # -----------------------------------------------------

    prompt = f"""
You are FitBuddy.

The user already has a 7-day workout plan.

Your task is to revise the workout plan according to the
user's feedback.

IMPORTANT RULES

1. Preserve the complete 7-day structure.

2. Only change portions of the workout that need to be
changed according to the user's feedback.

3. Continue including:

- Warm-ups
- Main exercises
- Sets and repetitions or duration
- Rest recommendations
- Cooldown or recovery

4. Maintain sensible workout progression.

5. Do not diagnose medical conditions.

6. Do not guarantee fitness results.

7. Return the COMPLETE revised 7-day plan.

8. Return plain text only.


ORIGINAL WORKOUT PLAN:

{original_plan}


USER FEEDBACK:

{feedback}


Generate the complete revised workout plan.
"""

    return generate_text(
        settings.gemini_workout_model,
        prompt,
    )