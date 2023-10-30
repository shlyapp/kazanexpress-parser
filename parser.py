import math
from typing import Dict, List
import requests
from config import products_headers, json_data, list_headers


def get_product_info(product_id) -> Dict:
    session = requests.Session()
    response = session.get(
            f'https://api.kazanexpress.ru/api/v2/product/{product_id}',
            headers=products_headers).json()
    info = {"name": response["payload"]["data"]["title"],
            "totalAvailableAmount": response["payload"]["data"]["totalAvailableAmount"],
            "photos": response["payload"]["data"]["photos"]
            }
    return info


def get_products(query: str) -> List:
    offset = 0
    session = requests.Session()
    response = session.post(
        'https://dshop.kznexpress.ru/',
        headers=list_headers,
        json=json_data(
            query,
            offset)).json()

    total_items = response.get('data').get('makeSearch').get('total')

    if total_items is None:
        return []

    pages_count = math.ceil(total_items / 48)    
    products = []
    
    for i in range(pages_count):
        offset = i * 48
        response = session.post(
            'https://dshop.kznexpress.ru/',
            headers=list_headers,
            json=json_data(
                query,
                offset)).json()
        products_id = response.get('data').get('makeSearch').get('items')
        for product in products_id:
            product_id = product.get('catalogCard').get('productId')
            product = get_product_info(product_id)
            products.append(product)
    
    return products
