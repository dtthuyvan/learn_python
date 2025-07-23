names = [3, 7]
names.append([1,2])
names.extend([1,2])
print(names)

numbers = [3, -7, 12, 4.5, 6.3]
sorted(numbers, reverse=True) #function creates a sorted version of the list but does not change the original list numbers
print(numbers)

scores = [89, 95, 72, 88]
scores.sort()
print(scores)

chars = list("python")
s = "-".join(chars)
print(s)

values = [2, 5, 7, 2, 8, 2]
values.extend([len(values), max(values)])
print(values)

nums = [5, 15, 25, 5, 15, 50, 5]
nums.remove(15)
print(nums)

l1 = [2, 4, 6, 2, 4, 12, 2]
l1.pop(3)
n = l1.count(2)
print(n)

l1 = [c.lower().upper() for c in 'PyThOn']
print(l1)

values = [5, 10, 15, 20, 25, 30]
filtered_values = [v for v in values if v > 15]
print(filtered_values)

words = ['apple', 'banana', 'cherry']
lengths = [len(w) * 3 for w in words]
print(lengths)

fruits = ['pear', 'mango', 'kiwi']
filtered_lengths = [len(f) for f in fruits if 'i' in f]
print(filtered_lengths)

team_a = ['Alice', 'Bob', 'Charlie']
team_b = ['Alice', 'David', 'Charlie']
x = [name for name in team_a if name in team_b]
print(x)

t1 = (1, 1.1, '1', (1, 3)) * 2
print(t1, t1[-1])

x = (1.4)
print(type(x))

my_tuple = tuple('Python')
#my_tuple[0] = 'X'
#print(my_tuple) #'tuple' object does not support item assignment

my_tuple = (1, 2, 3, 1, 2, 3)
print(my_tuple.count(1))

my_tuple = tuple('I-love-Python')
print(my_tuple[::3])
