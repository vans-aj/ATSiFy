import numpy as np
from sentence_transformers import SentenceTransformer

from backend.utils.file_utils import log_warning


def compute_cosine_similarity(
    text_a: str,
    text_b: str,
    embedder: SentenceTransformer,
    *,
    max_length: int = 0,
    context: str = "similarity",
) -> float:
    if not text_a or not text_b:
        return 0.0
    try:
        if max_length > 0:
            text_a = text_a[:max_length]
            text_b = text_b[:max_length]
        vec_a = embedder.encode(text_a, convert_to_tensor=False)
        vec_b = embedder.encode(text_b, convert_to_tensor=False)
        similarity = np.dot(vec_a, vec_b) / (
            np.linalg.norm(vec_a) * np.linalg.norm(vec_b)
        )
        return float(np.clip(similarity, 0.0, 1.0))
    except Exception as e:
        log_warning(f"Similarity error: {e}", context=context)
        return 0.0
