device = {'model': 7890, 'type': 'Smartphone'}
print(7890 in device) # it checks if that value is a key in the dictionary, which it isn't

dict1 = {2:5, 4:'6'}
dict1.update({10:'9'})
for k, v in dict1.items():
    print(f'{k*3} {v*3}')

my_dict = {2:3, 4:'5'}
#print(max(my_dict.values())) #TypeError: '5' is str

contact = {'name': 'Alice', 'city': 'Berlin', 'email': 'alice@email.com'}
print('name' in contact)
print('city' in contact.keys())
print(('city', 'Berlin') in contact.items())

contact = {'name': 'Alice', 'city': 'Berlin', 'email': 'alice@email.com'}
del contact['name']
print(contact.popitem())
print(contact)

revenue = {2023: 150_000, 2024: 250_000, 2025: 350_000}
profit = {k:v*0.15 for k,v in revenue.items()}
print(profit)

numbers = list(range(3))
letters = 'xyz'
d1 = dict(zip(numbers, letters))
print(d1)

config1 = {'theme': 'light', 'volume': 50}
config2 = {'volume': 70, 'brightness': 80}
 
merged_config = config1 | config2
print(merged_config)

settings = {'mode': 'auto', 'speed': 'fast'}
updates = {'speed': 'slow', 'resolution': 'high'}
 
settings |= updates
print(settings)