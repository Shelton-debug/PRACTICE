food_items = input('Enter food item name: ')

food_item_dict = {
    'burger': 50,
    'pizza': 100,
    'pasta': 80,
    'salad': 40,
    'sushi': 120,
    'juice': 30,
    'coffee': 20
}

def get_price(food_items):
    return food_item_dict.get(food_items, 'Item not found')

price = get_price(food_items)
print(f'The price of {food_items} is: {price}')