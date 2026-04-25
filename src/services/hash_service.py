import hashlib


def build_comments_signature(comments_list):
    """
    ساخت یک hash یکتا از لیست کامنت‌ها
    """
    if not comments_list:
        return None

    normalized_comments = [str(comment).strip() for comment in comments_list]
    normalized_comments.sort()

    combined_text = "||".join(normalized_comments)

    return hashlib.md5(combined_text.encode("utf-8")).hexdigest()