"""This is for printing list"""
def print_lol(the_list):
    """Explain about function """
    for each in the_list:
        if isinstance(each, list):
            print_lol(each)
        else:
            print(each)
