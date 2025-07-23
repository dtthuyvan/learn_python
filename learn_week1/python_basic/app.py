import simple_function
from class_and_obj import Member

z = lambda x, y: x + y
print(z(4,5))

simple_function.my_function('van', '35', 'Tan Phu')
simple_function.my_function('vi', '39')

print(simple_function.my_func_with_lambda(8))
print(simple_function.map_list_use_lambda([8, 10, 12,6]))

mem1 = Member('Van', 35, '2025-07-02')
mem2 = Member('Vi', 39, '2025-08-02', 'HCM')
print(mem1)
print(mem2)