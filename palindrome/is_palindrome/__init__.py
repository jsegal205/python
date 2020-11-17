def is_palindrome(input_var):
    if type(input_var) == int:
        slim = str(input_var)
    elif type(input_var) == str:
        slim = input_var.lower().replace(" ", "")
    elif type(input_var) == list:
        slim = [s.lower() for s in input_var]
    else:
        slim = input_var

    return slim == slim[::-1]
