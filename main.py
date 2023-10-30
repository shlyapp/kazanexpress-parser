import json
from parser import get_products


input_query = input("Введите название товара: ")

products = get_products(input_query)

if len(products) == 0:
    print("Товаров по вашему запросу не найдено.")
else:
    json = json.dumps(products, ensure_ascii=False)
    with open('data.json', 'w') as file:
        file.write(json)
    print("Данные о товарах записаны в файл 'data.json'")

