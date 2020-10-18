__author__ = 'ArkJzzz (arkjzzz@gmail.com)'

import logging
import os
import requests
import json

from datetime import datetime
from dotenv import load_dotenv


logger = logging.getLogger('cms_helpers')

BASE_URL = 'https://api.moltin.com/v2'


def get_moltin_api_token():
    load_dotenv()
    moltin_client_id = os.getenv('ELASTICPATH_CLIENT_ID')
    url = 'https://api.moltin.com/oauth/access_token'
    data = {
      'client_id': moltin_client_id,
      'grant_type': 'implicit'
    }
    response = requests.post(url, data=data)
    response.raise_for_status()

    moltin_autorization_data = response.json()
    logger.debug(moltin_autorization_data)

    moltin_api_token = '{} {}'.format(
            moltin_autorization_data['token_type'],
            moltin_autorization_data['access_token'],
        )
    expires = int(moltin_autorization_data['expires'])
    expires_in = int(moltin_autorization_data['expires_in'])
    expire_in = expires_in + expires
    expire_in = (
        datetime.utcfromtimestamp(expire_in).strftime('%Y-%b-%d %H:%M:%S (UTC)')
    )
    logger.info('token expire on: {}'.format(expire_in))

    os.environ['MOLTIN_API_TOKEN'] = moltin_api_token

    return moltin_api_token


def get_products(moltin_api_token):
    url = '{base_url}/products/'.format(
        base_url=BASE_URL,
        )
    headers = {
        'Authorization': moltin_api_token,
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()


def get_product(moltin_api_token, product_id):
    url = '{base_url}/products/{product_id}'.format(
                    base_url=BASE_URL,
                    product_id=product_id,
                )
    headers = {
        'Authorization': moltin_api_token,
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()


def get_all_files(moltin_api_token):
    url = '{base_url}/files'.format(
            base_url=BASE_URL,
        )
    headers = {
        'Authorization': moltin_api_token,
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()


def get_image_link(moltin_api_token, image_id):
    url = '{base_url}/files/{image_id}'.format(
            base_url=BASE_URL,
            image_id=image_id,
        )
    headers = {
        'Authorization': moltin_api_token,
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    file_data = response.json()

    return file_data['data']['link']['href']


def add_product_to_cart(moltin_api_token, chat_id, product_id, quantity):
    url = '{base_url}/carts/{cart_id}/items'.format(
            base_url=BASE_URL,
            cart_id=chat_id,
        )
    headers = {
        'Authorization': moltin_api_token,
        'Content-Type': 'application/json',
    }
    payload = {
        'data': { 
            'id': product_id,
            'type': 'cart_item',
            'quantity': quantity,
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()


def get_cart(moltin_api_token, chat_id):
    url = '{base_url}/carts/{cart_id}'.format(
            base_url=BASE_URL,
            cart_id=chat_id,
        )
    headers = {
        'Authorization': moltin_api_token,
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()


def get_cart_items(moltin_api_token, chat_id):
    url = '{base_url}/carts/{cart_id}/items'.format(
            base_url=BASE_URL,
            cart_id=chat_id,
        )
    headers = {
        'Authorization': moltin_api_token,
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()


def delete_cart(moltin_api_token, chat_id):
    url = '{base_url}/carts/{cart_id}'.format(
            base_url=BASE_URL,
            cart_id=chat_id,
        )
    headers = {
        'Authorization': moltin_api_token,
    }
    response = requests.delete(url, headers=headers)
    response.raise_for_status()

    return response


def get_cart_items(moltin_api_token, chat_id):
    url = '{base_url}/carts/{cart_id}/items'.format(
            base_url=BASE_URL,
            cart_id=chat_id,
        )
    headers = {
        'Authorization': moltin_api_token,
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()


def remove_cart_item(moltin_api_token, chat_id, item_id):
    url = '{base_url}/carts/{cart_id}/items/{item_id}'.format(
            base_url=BASE_URL,
            cart_id=chat_id,
            item_id=item_id,
        )
    headers = {
        'Authorization': moltin_api_token,
        'Content-Type': 'application/json',
        }
    response = requests.delete(url, headers=headers)
    response.raise_for_status()

    return response.json()


def create_customer(moltin_api_token, customer_name, email):
    url = '{base_url}/customers'.format(
            base_url=BASE_URL,
        )
    headers = {
        'Authorization': moltin_api_token,
        'Content-Type': 'application/json',
    }
    payload = {
        'data': { 
            'type': 'customer',
            'name': customer_name,
            'email': email,
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()


if __name__ == '__main__':
    logger.error('Этот скрипт не предназначен для запуска напрямую')