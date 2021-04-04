def query_model(
    model, 
    hash_key, 
    range_key_condition=None, 
    filter_condition=None
    ):

    def iterate_over_page(
        model, 
        hash_key,
        results,
        range_key_condition=None, 
        filter_condition=None,
        last_evaluated_key = None,

        ):
        items = model.query(hash_key, range_key_condition, filter_condition, last_evaluated_key=last_evaluated_key)
        
        for item in items:
            results.append(item)

        return items.last_evaluated_key

    if not model or hash_key:
        return
        
    results = []

    last_evaluated_key = iterate_over_page(model, hash_key, results, range_key_condition, filter_condition)

    while last_evaluated_key:
        last_evaluated_key = iterate_over_page(model, hash_key, results, range_key_condition, filter_condition, last_evaluated_key)

    return results