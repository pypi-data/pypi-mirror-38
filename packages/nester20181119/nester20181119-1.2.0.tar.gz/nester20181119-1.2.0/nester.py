""" This is "nester.py" module and it provides one function called print_lol()
which prints lists that may or may not include nested lists.
A second argument called “level" is used to insert tab-stops when a nested list is encountered."""
def print_lol(the_list, level=0):
    """ my module print list in list, in list
    in list..... etc """
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end='')
            print(each_item)
