import random
import time
from functools import lru_cache

from google import genai
from google.genai import errors

from ..config import get_settings


@lru_cache
def get_client():
    settings = get_settings()

    if settings.mock_ai:
        return None

    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Add your Gemini API key to .env."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_text(
    model: str,
    prompt: str,
    max_retries: int = 5,
) -> str:

    client = get_client()

    if client is None:
        raise RuntimeError(
            "Gemini is disabled because MOCK_AI=true."
        )

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )

            text = (response.text or "").strip()

            if not text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return text

        except errors.ServerError as exc:

            # Retry only temporary Gemini server errors
            # such as 500, 502, 503 and 504.

            status_code = getattr(
                exc,
                "code",
                None,
            )

            if status_code not in (
                500,
                502,
                503,
                504,
            ):
                raise

            if attempt == max_retries - 1:
                raise RuntimeError(
                    "Gemini is temporarily busy. "
                    "Please try again in a few minutes."
                ) from exc

            # Exponential backoff:
            # approximately 2, 4, 8, 16 seconds
            delay = (2 ** (attempt + 1)) + random.uniform(0, 1)

            print(
                f"Gemini temporarily unavailable "
                f"(HTTP {status_code}). "
                f"Retrying in {delay:.1f} seconds..."
            )

            time.sleep(delay)

        except errors.ClientError:
            # 4xx errors normally indicate problems such as
            # authentication, quota, request format, etc.
            raise