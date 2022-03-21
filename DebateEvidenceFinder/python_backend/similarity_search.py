def find_top_similarity(query, cards, has_id): #(id, <card_object>)/<card_object>
    similarities = []
    if has_id:
        for id_, card in cards:
            similarities.append((id_, (card.find_similarity(query), card)))
        similarities = sorted(similarities, key=lambda tup: tup[1][0])[::-1]
    else:
        for card in cards:
            similarities.append((card.find_similarity(query), card))
        similarities = sorted(similarities, key=lambda tup: tup[0])[::-1]
    return similarities