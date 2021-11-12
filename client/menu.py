def menu():
    """
    return the list of the numbers given by the user
    """
    cont = True  # Var to retry if there is more than 10 values

    list_num = []  # List of numbers

    while cont:
        values = input("Enter integers separated by spaces (max 10), enter quit to exit: ")
        if values.lower() == 'quit':
            return 0
        list_str_value = values.split()
        if len(list_str_value) < 11:
            cont = False
            list_num = values
        else:
            print("There is to many number (max 10) please retry")
    return list_num
