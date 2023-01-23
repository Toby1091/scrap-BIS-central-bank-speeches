def reorder_found_strings(found_strings, search_string):
    """
    @found_strings: list of strings (all of which must be contained within search_string)
    @search_string: string
    @return: returns found_strings, ordered by the index in which the string occor in search_string
    @note: all strings are converted to lowercase before searching.
    """
    order_dict = {}
    for found_string in found_strings:
        index = search_string.lower().index(found_string.lower())
        order_dict[index] = found_string
    return [order_dict[index] for index in sorted(order_dict.keys())]
