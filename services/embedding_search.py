import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")


def product_to_text(product) -> str:
    parts = [
        product.title,
        product.brand,
        product.category,
        product.style,
        product.color,
        product.gender,
        product.size,
        product.material,
        str(product.price),
        product.store,
        product.description,
    ]

    return " ".join([str(part) for part in parts if part])


def cosine_similarity(vec1, vec2) -> float:
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))


def semantic_rank_products(user_query: str, products: list):
    if not products:
        return []

    query_embedding = model.encode(user_query)

    ranked_products = []

    for product in products:
        product_text = product_to_text(product)
        product_embedding = model.encode(product_text)

        score = cosine_similarity(query_embedding, product_embedding)
        setattr(product, "score", round(score, 4))

        ranked_products.append(product)

    return sorted(ranked_products, key=lambda x: x.score, reverse=True)