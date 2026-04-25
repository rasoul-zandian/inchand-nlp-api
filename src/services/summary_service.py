from datetime import datetime
from src.storage.file_store import save_summary_record, get_summary_record
from src.services.hash_service import build_comments_signature
from src.services.llm_service import generate_llm_summary


def build_fallback_summary(comments_list):
    preview = " | ".join(comments_list[:3]) if comments_list else None

    return {
        "summary": preview,
        "pros": [],
        "cons": [],
        "sentiment_overview": "mixed"
    }


MIN_COMMENTS_FOR_LLM = 3


def generate_summary_with_llm(product_id: str, product_comments_df):
    """
    ساخت summary حرفه‌ای با استفاده از LLM (در صورت کافی بودن داده)
    """
    if product_comments_df.empty:
        return {
            "product_id": product_id,
            "status": "no_comments",
            "summary": None,
            "pros": [],
            "cons": [],
            "sentiment_overview": None,
            "comment_count": 0,
            "is_cached": False,
            "message": "No comments available for this product.",
            "last_generated_at": None,
            "comments_hash": None
        }

    comments_list = product_comments_df["comment_text"].dropna().tolist()
    comment_count = len(comments_list)
    comments_hash = build_comments_signature(comments_list)

    # 👇 قانون جدید
    if comment_count < MIN_COMMENTS_FOR_LLM:

        if comment_count == 1:
            status = "single_comment"
            message = "Only one comment available. No summarization needed."
        else:
            status = "few_comments"
            message = "Not enough comments for meaningful summarization."

        preview = " | ".join(comments_list)

        summary_data = {
            "product_id": product_id,
            "status": status,
            "summary": preview,
            "pros": [],
            "cons": [],
            "sentiment_overview": "mixed",
            "comment_count": comment_count,
            "is_cached": False,
            "message": message,
            "last_generated_at": datetime.utcnow().isoformat(),
            "comments_hash": comments_hash
        }

        save_summary_record(product_id, summary_data)
        return summary_data

    # 👇 اگر داده کافی بود → LLM
    try:
        llm_result = generate_llm_summary(comments_list)
        message = "Summary generated with LLM."
        status = "ready"

    except Exception:
        llm_result = build_fallback_summary(comments_list)
        message = "LLM failed. Fallback summary was generated."
        status = "fallback"

    summary_data = {
        "product_id": product_id,
        "status": status,
        "summary": llm_result.get("summary"),
        "pros": llm_result.get("pros", []),
        "cons": llm_result.get("cons", []),
        "sentiment_overview": llm_result.get("sentiment_overview"),
        "comment_count": comment_count,
        "is_cached": False,
        "message": message,
        "last_generated_at": datetime.utcnow().isoformat(),
        "comments_hash": comments_hash
    }

    save_summary_record(product_id, summary_data)

    return summary_data


def get_or_create_summary(product_id: str, product_comments_df):
    """
    اگر summary قبلاً ذخیره شده و هنوز معتبر باشد، همان را برگردان.
    در غیر این صورت summary جدید با LLM بساز.
    """
    comments_list = product_comments_df["comment_text"].dropna().tolist()
    current_hash = build_comments_signature(comments_list)

    existing_summary = get_summary_record(product_id)

    if existing_summary:
        stored_hash = existing_summary.get("comments_hash")

        if stored_hash == current_hash:
            existing_summary["is_cached"] = True
            existing_summary["message"] = "Summary returned from valid cache."
            return existing_summary

    return generate_summary_with_llm(product_id, product_comments_df)


def force_refresh_summary(product_id: str, product_comments_df):
    """
    بدون توجه به cache، summary را دوباره بساز
    """
    return generate_summary_with_llm(product_id, product_comments_df)


def get_summary_status(product_id: str, product_comments_df):
    """
    فقط وضعیت summary را برگردان
    """
    if product_comments_df.empty:
        return {
            "product_id": product_id,
            "status": "no_comments",
            "has_summary": False,
            "comment_count": 0,
            "is_cached": False,
            "last_generated_at": None,
            "message": "No comments available for this product."
        }

    comments_list = product_comments_df["comment_text"].dropna().tolist()
    current_hash = build_comments_signature(comments_list)

    existing_summary = get_summary_record(product_id)

    if not existing_summary:
        return {
            "product_id": product_id,
            "status": "missing",
            "has_summary": False,
            "comment_count": len(comments_list),
            "is_cached": False,
            "last_generated_at": None,
            "message": "No stored summary found for this product."
        }

    stored_hash = existing_summary.get("comments_hash")

    if stored_hash == current_hash:
        return {
            "product_id": product_id,
            "status": "ready",
            "has_summary": True,
            "comment_count": len(comments_list),
            "is_cached": True,
            "last_generated_at": existing_summary.get("last_generated_at"),
            "message": "Stored summary is valid."
        }

    return {
        "product_id": product_id,
        "status": "stale",
        "has_summary": True,
        "comment_count": len(comments_list),
        "is_cached": False,
        "last_generated_at": existing_summary.get("last_generated_at"),
        "message": "Stored summary is outdated and should be regenerated."
    }