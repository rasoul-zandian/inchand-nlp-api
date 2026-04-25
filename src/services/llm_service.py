import json
from openai import OpenAI
from src.core.config import OPENAI_API_KEY, OPENAI_MODEL


client = OpenAI(api_key=OPENAI_API_KEY)


def build_summary_prompt(comments_list):
    comments_text = "\n".join(comments_list)

    prompt = f"""
شما یک تحلیل‌گر حرفه‌ای تجربه مشتری هستید.

در ادامه، نظرات کاربران درباره یک محصول را می‌بینید:

{comments_text}

لطفاً فقط بر اساس همین نظرات، خروجی را دقیقاً به صورت JSON معتبر برگردان.
هیچ متن اضافه‌ای قبل یا بعد از JSON ننویس.

فرمت خروجی باید دقیقاً این باشد:

{{
  "summary": "یک جمع‌بندی کوتاه و حرفه‌ای 3 تا 5 خطی",
  "pros": ["نقطه قوت 1", "نقطه قوت 2", "نقطه قوت 3"],
  "cons": ["نقطه ضعف 1", "نقطه ضعف 2"],
  "sentiment_overview": "mostly_positive"
}}

قواعد:
- فقط از اطلاعات موجود در نظرات استفاده کن
- pros و cons کوتاه و مشخص باشند
- sentiment_overview فقط یکی از این مقادیر باشد:
  mostly_positive
  mostly_negative
  mixed
"""

    return prompt


def validate_llm_output(data):
    required_keys = ["summary", "pros", "cons", "sentiment_overview"]

    if not isinstance(data, dict):
        raise ValueError("LLM output is not a valid dictionary.")

    for key in required_keys:
        if key not in data:
            raise ValueError(f"Missing key in LLM output: {key}")

    if not isinstance(data["pros"], list):
        raise ValueError("Field 'pros' must be a list.")

    if not isinstance(data["cons"], list):
        raise ValueError("Field 'cons' must be a list.")

    if data["sentiment_overview"] not in ["mostly_positive", "mostly_negative", "mixed"]:
        raise ValueError("Invalid value for sentiment_overview.")

    return data


def generate_llm_summary(comments_list):
    prompt = build_summary_prompt(comments_list)

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        content = response.choices[0].message.content.strip()
        parsed = json.loads(content)
        validated = validate_llm_output(parsed)

        return validated

    except Exception as e:
        raise RuntimeError(f"LLM summary generation failed: {str(e)}")