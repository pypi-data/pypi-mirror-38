def print_list(new_lists):
    for new_list in new_lists:
        if isinstance(new_list, list):
            print_list(new_list)
            # return print_list(new_list)
        else:
            print(new_list)





