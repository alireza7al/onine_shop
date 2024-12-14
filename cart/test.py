data = {
    "session_key": {
        "1": {"price": 100, "quantity": 1},
        "2": {"price": 400, "quantity": 44},
        "3": {"price": 200, "quantity": 2},
        "4": {"price": 20000, "quantity": 3}
    }}
x = (data.get('session_key'))
# {'1': {'price': 100, 'quantity': 1}, '2': {'price': 400, 'quantity': 44}, '3': {'price': 200, 'quantity': 2},
# '4': {'price': 20000, 'quantity': 3}}

sum = 0
for i in x:
    sum = sum + ((x.get(i).get('price')) * (x.get(i).get('quantity')))
    print(sum)
