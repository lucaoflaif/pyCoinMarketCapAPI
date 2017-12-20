"""This module contains some functions useful for coinmarketcapapi package
"""

def dicts_filter(dicts_object, field_to_filter, value_of_filter):
    """This function gets as arguments an array of dicts through the dicts_objects parameter,
       then it'll return the dicts that have a value value_of_filter of the key field_to_filter.
    """
    lambda_query = lambda value: value[field_to_filter] == value_of_filter

    filtered_coin = filter(lambda_query, dicts_object)
    selected_coins = list(filtered_coin)
    #if not selected_coin: #Empty list, no coin found
    #    raise AttributeError('attribute %s not found' % attr)
    return selected_coins
