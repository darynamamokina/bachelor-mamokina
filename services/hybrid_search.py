from services.ranking import calculate_score
from services.embedding_search import semantic_rank_products


def hybrid_rank_products(user_query, products, parsed):
    if not products:
        return []

    semantic_products = semantic_rank_products(
        user_query,
        products
    )

    ranked_products = []

    for product in semantic_products:
        rule_score = calculate_score(
            product,
            parsed
        )

        normalized_rule_score = min(
            rule_score / 10,
            1
        )

        semantic_score = getattr(
            product,
            "score",
            0
        )

        final_score = (
            normalized_rule_score * 0.5 +
            semantic_score * 0.5
        )

        setattr(
            product,
            "score",
            round(final_score, 4)
        )

        ranked_products.append(product)

    return sorted(
        ranked_products,
        key=lambda x: x.score,
        reverse=True
    )