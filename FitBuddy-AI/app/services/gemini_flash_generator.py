from ..config import get_settings
from .gemini_client import generate_text


def generate_nutrition_tip_with_flash(
    goal: str,
) -> str:

    settings = get_settings()

    # -----------------------------------------------------
    # MOCK MODE
    # -----------------------------------------------------

    if settings.mock_ai:

        return (
            f"For {goal}, build meals around protein, "
            "vegetables or fruit, minimally processed "
            "carbohydrates, healthy fats and adequate water. "
            "Adjust portions according to your individual "
            "needs and preferences."
        )

    # -----------------------------------------------------
    # GEMINI PROMPT
    # -----------------------------------------------------

    prompt = f"""
You are FitBuddy.

Provide one concise and practical nutrition or recovery
tip for someone whose fitness goal is:

{goal}

Requirements:

- Keep the answer between 2 and 4 sentences.
- Make the advice easy to understand.
- Avoid medical diagnosis.
- Avoid extreme dieting recommendations.
- Avoid supplement prescriptions.
- Do not guarantee fitness results.
- Mention that individual nutritional needs can vary
  when appropriate.

Return only the nutrition/recovery advice.
"""

    return generate_text(
        settings.gemini_tip_model,
        prompt,
    )