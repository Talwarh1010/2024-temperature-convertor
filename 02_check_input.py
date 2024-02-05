def check_temp(min_value):
    error = f"Please enter a number that is more than {min_value}"
    try:
        response = float(input("Choose a number: "))
        if response < min_value:
            print(error)
        else:
            return response
    except ValueError:
        print(error)


while True:
    check_temp(-273)
