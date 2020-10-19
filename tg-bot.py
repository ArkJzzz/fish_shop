__author__ = 'ArkJzzz (arkjzzz@gmail.com)'

import os
import logging
import redis
import requests
import json

from telegram import InlineKeyboardMarkup
from telegram.ext import Filters
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import MessageHandler
from dotenv import load_dotenv
from validate_email import validate_email

import cms_helpers
import keyboards


logger = logging.getLogger(__file__)

_database = None


def main():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
            fmt='%(asctime)s %(name)s:%(lineno)d - %(message)s',
            datefmt='%Y-%b-%d %H:%M:%S (%Z)',
            style='%',
        )
    console_handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

    cms_helpers_logger = logging.getLogger('cms_helpers')
    cms_helpers_logger.addHandler(console_handler)
    cms_helpers_logger.setLevel(logging.DEBUG)

    keyboards_logger = logging.getLogger('keyboards')
    keyboards_logger.addHandler(console_handler)
    keyboards_logger.setLevel(logging.DEBUG)

    load_dotenv()
    token = os.getenv('TELEGRAM_TOKEN')
    updater = Updater(token, use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', handle_users_reply))
    dispatcher.add_handler(CallbackQueryHandler(handle_users_reply))
    dispatcher.add_handler(MessageHandler(Filters.text, confirm_email))

    updater.start_polling()
    updater.idle()


def get_database_connection():
    global _database
    if _database is None:
        database_password = os.getenv('REDIS_PASSWORD')
        database_host = os.getenv('REDIS_HOST')
        database_port = os.getenv('REDIS_PORT')
        _database = redis.Redis(
                host=database_host,
                port=database_port,
                password=database_password,
            )
    return _database


def handle_users_reply(update, context):
    db = get_database_connection()

    if update.message:
        user_reply = update.message.text
        chat_id = update.message.chat_id
    elif update.callback_query:
        callback_data = json.loads(update.callback_query.data)
        user_reply = callback_data[0]
        chat_id = update.callback_query.message.chat_id
    else:
        return

    if user_reply == '/start':
        user_state = 'START'
    elif user_reply =='HANDLE_MENU':
        user_state = 'HANDLE_MENU'
    elif user_reply == 'HANDLE_DESCRIPTION':
        user_state = 'HANDLE_DESCRIPTION'
    elif user_reply == 'CLEAR_CART':
        user_state = 'CLEAR_CART'
    elif user_reply == 'HANDLE_CART':
        user_state = 'HANDLE_CART'
    elif user_reply == 'HANDLE_REMOVE_ITEM':
        user_state = 'HANDLE_CART'
    elif user_reply == 'HANDLE_CHECKOUT':
        user_state = 'WAITING_EMAIL'
    elif user_reply == 'HANDLE_CREATE_CUSTOMER':
        user_state = 'WAITING_EMAIL'
    else:
        user_state = db.hget(
            name='fish_shop_users_states',
            key=chat_id,
        ).decode("utf-8")

    logger.debug('user_state: {}'.format(user_state))
    
    states_functions = {
        'START': start,
        'HANDLE_MENU': show_menu,
        'HANDLE_DESCRIPTION': show_description,
        'HANDLE_CART': show_cart,
        'WAITING_EMAIL': checkout,
    }

    state_handler = states_functions[user_state]

    try:
        next_state = state_handler(update, context)
        logger.debug('next_state: {}\n'.format(next_state))
        db.hset(name='fish_shop_users_states', key=chat_id, value=next_state)
        

    except requests.exceptions.HTTPError as err:
        status_code = err.response.status_code
        logger.error('Error. Status code {}'.format(status_code))
        if status_code == 403:
            cms_helpers.get_moltin_api_token()
        elif status_code == 409:
            logger.warning('Такой e-mail уже есть в базе')
            exeption_409(update, context)

    except Exception as err:
        logger.error('Error: {}'.format(err), exc_info=True)

def error(update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def exeption_409(update, context):
    query = update.callback_query
    query.message.reply_text(
            text='Такой e-mail уже есть в базе, попробуйте заново',
        )

    return 'WAITING_EMAIL'


def start(update, context):
    chat_id = update.message.chat_id
    user = update.message.from_user
    logger.info('User @{} started the conversation.'.format(user.username))
    moltin_api_token = cms_helpers.get_moltin_api_token()
    logger.debug('Moltin API token: {}'.format(moltin_api_token))
    cart = cms_helpers.get_cart(moltin_api_token, chat_id)
    logger.debug('Корзина: {}'.format(cart))

    welcome_message = 'Здравствуйте, {}\n'\
            'Рады видеть Вас в нашем магазине!\n'\
            'Загляните в наше меню:'\
        .format(user.first_name)
    reply_keyboard = InlineKeyboardMarkup(keyboards.start_keyboard)

    update.message.reply_text(
        text=welcome_message, 
        reply_markup=reply_keyboard,
    )

    return 'HANDLE_MENU'


def show_menu(update, context):
    query = update.callback_query
    callback_data = json.loads(query.data)
    user_reply = callback_data[0]
    moltin_api_token = os.getenv('MOLTIN_API_TOKEN')
    products = cms_helpers.get_products(moltin_api_token)

    if user_reply == 'HANDLE_MENU':
        reply_keyboard = keyboards.get_menu_keyboard(products['data'])
        reply_keyboard = InlineKeyboardMarkup(reply_keyboard)
        context.bot.delete_message(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
        )
        query.message.reply_text(
            text='В нашем магазине Вы можете купить следующие товары:',
            reply_markup=reply_keyboard,
        )
    else: 
        logger.debug(query.data)

    return 'HANDLE_DESCRIPTION'


def show_description(update, context):
    moltin_api_token = os.getenv('MOLTIN_API_TOKEN')
    query = update.callback_query
    chat_id = query.message.chat_id
    callback_data = json.loads(query.data)
    user_reply = callback_data[0]

    if user_reply == 'HANDLE_DESCRIPTION':
        product_id = callback_data[1]
        product_data = cms_helpers.get_product(moltin_api_token, product_id)
        image_id = (product_data['data']['relationships']
                                                ['main_image']['data']['id'])
        image_link = cms_helpers.get_image_link(moltin_api_token, image_id)
        message = keyboards.format_product_info(product_data)
        product_details_keyboard = keyboards.get_product_details_keyboard(
                product_id,
            )
        reply_keyboard = InlineKeyboardMarkup(product_details_keyboard)

        context.bot.delete_message(
            chat_id=chat_id,
            message_id=query.message.message_id,
        )
        context.bot.send_photo(
            chat_id=chat_id,
            photo=image_link,
            caption=message,
            reply_markup=reply_keyboard,
        )

    elif user_reply == 'ADD_TO_CART':
        product_id = callback_data[1]
        quantity = callback_data[2]
        adding_result = cms_helpers.add_product_to_cart(
                moltin_api_token,
                chat_id,
                product_id,
                quantity,
            )
        logger.debug(
            'Результат добавления товара в корзину: {}'.format(
                adding_result
            )
        )

    else: 
        logger.debug(query.data)

    return 'HANDLE_DESCRIPTION'


def show_cart(update, context):
    moltin_api_token = os.getenv('MOLTIN_API_TOKEN')
    query = update.callback_query
    chat_id = query.message.chat_id
    callback_data = json.loads(query.data)
    user_reply = callback_data[0]

    if user_reply == 'HANDLE_REMOVE_ITEM':
        item_id = callback_data[1]
        logger.debug('Удаление товара с id {}'.format(item_id))
        cms_helpers.remove_cart_item(moltin_api_token, chat_id, item_id)

    cart_items = cms_helpers.get_cart_items(moltin_api_token, chat_id)
    formated_cart_items = keyboards.format_cart(cart_items)
    cart_show_keyboard = keyboards.get_cart_show_keyboard(cart_items)
    cart_show_keyboard = InlineKeyboardMarkup(cart_show_keyboard)
    logger.debug('Товары в корзине: {}'.format(cart_items))

    context.bot.delete_message(
        chat_id=chat_id,
        message_id=query.message.message_id,
    )
    query.message.reply_text(
        text=formated_cart_items,
        reply_markup=cart_show_keyboard,
    )
    
    return 'HANDLE_CART'


def checkout(update, context):
    moltin_api_token = os.getenv('MOLTIN_API_TOKEN')
    query = update.callback_query
    chat_id = query.message.chat_id
    customer_name = query.from_user.first_name
    callback_data = json.loads(query.data)
    user_reply = callback_data[0]

    context.bot.delete_message(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
    )

    if user_reply == 'HANDLE_CHECKOUT':
        waiting_email_message = 'Напишите, пожалуйста, Ваш e-mail адрес'
        query.message.reply_text(
            text=waiting_email_message,
        )

        return 'WAITING_EMAIL'

    elif user_reply == 'HANDLE_CREATE_CUSTOMER':
        customer_email = callback_data[1]
        cart_items = cms_helpers.get_cart_items(moltin_api_token, chat_id)
        customer = cms_helpers.create_customer(
                moltin_api_token, 
                customer_name, 
                customer_email
            )

        buy_message = 'Совершена покупка:\n'\
            '{customer}\n\n'\
            '{cart_items}\n'\
            .format(
                customer=customer['data'],
                cart_items=keyboards.format_cart(cart_items),
            )
        logger.info(buy_message)
        context.bot.send_message(
            chat_id=os.getenv('ADMIN_CHAT_ID'),
            text=buy_message
            )

        create_customer_message = 'Спасибо за покупку!\n'\
                'Мы с Вами свяжемся в ближайшее время '\
                'для уточнения способа оплаты и доставки выбранных товаров'
        reply_keyboard = InlineKeyboardMarkup(keyboards.start_keyboard)
        query.message.reply_text(
            text=create_customer_message,
            reply_markup=reply_keyboard,
        )

        return 'HANDLE_MENU'

    else: 
        logger.debug(query.data)

        return 'WAITING_EMAIL'


def confirm_email(update, context):
    user_reply = update.message.text
    logger.debug('user_reply: {}'.format(user_reply))

    if validate_email(user_reply):
        confirmation_keyboard = keyboards.get_confirmation_keyboard(user_reply)
        reply_keyboard = InlineKeyboardMarkup(confirmation_keyboard)
        update.message.reply_text(
            text='ваш e-mail: {}'.format(user_reply), 
            reply_markup=reply_keyboard,
        )
    else:
        invalid_email_message = 'Кажется, e-mail неправильный.\n'\
                                'Попробуйте снова.'
        update.message.reply_text(
            text=invalid_email_message, 
        )

    return 'WAITING_EMAIL'


if __name__ == '__main__':
    main()
