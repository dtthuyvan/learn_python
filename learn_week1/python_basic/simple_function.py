def my_function(name, age, address = 'None'):
    print(f"Name {name}, age {age}, address {address}")

def my_func_with_lambda(num):
    double = lambda x: x * 2
    return double(num)

def map_list_use_lambda(list_num):
    new_list = list(map(lambda x: x * 2, list_num))
    return new_list