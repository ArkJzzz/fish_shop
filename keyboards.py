__author__ = 'ArkJzzz (arkjzzz@gmail.com)'


import json
import logging

from telegram import InlineKeyboardButton

logger = logging.getLogger('keyboards')


start_keyboard = [
    [
        InlineKeyboardButton(
            text='Меню магазина', 
            callback_data=json.dumps(['HANDLE_MENU']),
        )
    ],
]


def get_menu_keyboard(products):
    menu_keyboard = []
    for product in products:
        product_name = product['name']
        product_id = product['id']
        callback_data = json.dumps(['HANDLE_DESCRIPTION', product_id,])

        menu_keyboard.append(
            [
                InlineKeyboardButton(
                    text=product_name, 
                    callback_data=callback_data,
                )
            ],
        )

    menu_keyboard.append(
        [
            InlineKeyboardButton(
                text='Показать корзину', 
                callback_data=json.dumps(['HANDLE_CART']),
            )
        ],
    )

    return menu_keyboard


def get_product_details_keyboard(product_id):
    product_details_keyboard = []
    quantities = [1, 2, 5]

    for quantity in quantities:
        product_details_keyboard.append(
            InlineKeyboardButton(
                text='+{} кг'.format(quantity), 
                callback_data=json.dumps(
                        ['ADD_TO_CART', product_id, quantity]
                    ),
            ),
        )
    product_details_keyboard = [product_details_keyboard]
    product_details_keyboard.append(            
        [
            InlineKeyboardButton(
                text='В меню', 
                callback_data=json.dumps(['HANDLE_MENU']),
            )
        ],
    )

    return product_details_keyboard


def get_cart_show_keyboard(cart_items):
    cart_show_keyboard = []
    for item in cart_items['data']:
        item_name = item['name']
        item_id = item['id']
        product_id = item['product_id']
        callback_data = json.dumps(['HANDLE_REMOVE_ITEM', item_id])
        cart_show_keyboard.append(
            [
                InlineKeyboardButton(
                    text='Удалить из корзины {}'.format(item_name),
                    callback_data=callback_data,
                )
            ],
        )
    cart_show_keyboard.append(
        [
            InlineKeyboardButton(
                text='Продолжить покупки', 
                callback_data=json.dumps(['HANDLE_MENU']),
            ),
            InlineKeyboardButton(
                text='Оформить заказ', 
                callback_data=json.dumps(['HANDLE_CHECKOUT']),
            ),
        ],
    )

    return cart_show_keyboard


def get_confirmation_keyboard(email):
    confirmation_keyboard = [
        [
            InlineKeyboardButton(
                text='Все верно', 
                callback_data=json.dumps(['HANDLE_CREATE_CUSTOMER', email]),
            )
        ],
        [
            InlineKeyboardButton(
                text='Ввести заново', 
                callback_data=json.dumps(['HANDLE_CHECKOUT']),
            ),
        ]
    ]

    return confirmation_keyboard


def format_product_info(product_data):
    product_data = product_data['data']
    product_meta = product_data['meta']

    product_name = product_data['name']
    description = product_data['description']
    display_price = product_meta['display_price']['with_tax']['formatted']
    availability = product_meta['stock']['level']

    formated_info = '{product_name}\n\n'\
        '{display_price} за килограмм\n'\
        '{description}'\
        .format(
            product_name=product_name,
            display_price=display_price,
            availability=availability,
            description=description,
        )

    return formated_info


def format_cart(cart_items):
    cart_price = cart_items['meta']['display_price']['with_tax']['formatted']
    cart_items_for_print = ''
    for item in cart_items['data']:
        item_display_price = item['meta']['display_price']['with_tax']
        cart_items_for_print += '{name}\n'\
        '{description}\n'\
        '{item_price} за килограмм\n'\
        'в корзине {quantity}кг на сумму {value}\n\n'\
        .format(
            name=item['name'],
            description=item['description'],
            quantity=item['quantity'],
            item_price=item_display_price['unit']['formatted'],
            value=item_display_price['value']['formatted'],
            )

    formated_cart = '{items}\nСумма заказа: {cart_price}'.format(
                items=cart_items_for_print,
                cart_price=cart_price,
            )

    return formated_cart

