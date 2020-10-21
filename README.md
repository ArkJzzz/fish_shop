# fish_shop

Чат-бот-магазин для Telegram.

![](tg-fish-shop.gif)


## Что используется 

- Интеграция по API с CMS [Elastic Path](https://www.elasticpath.com/) (ранее Moltin)
- Отслеживание действий пользователя с помощью конечного автомата (Finite-State Machine)
- Inline кнопки
- Отправка изображений в чат


## Подготовка

- **Elastic Path**
    
    Зарегистрируйтесь на [Elastic Path](https://www.elasticpath.com/).

    Получите [ключи для доступа к API](https://dashboard.elasticpath.com/app).

    ![](elasticpath_keys.png)


    Создайте товары [в каталоге товаров](https://dashboard.elasticpath.com/app/catalogue/products)

    ![](elasticpath_catalogue.png)


- **Telegram**

    Напишите [Отцу ботов](https://telegram.me/BotFather):

    ```
    \start
    ```

    ```
    \newbot
    ```

    Получите токен для доступа к API Telegram.

- **Redis**

    Зарегистрируйтесь на [redislabs](https://redislabs.com/).

    Получите адрес БД вида `redis-13965.f18.us-east-4-9.wc1.cloud.redislabs.com`, его порт вида: `16635` и его пароль.


## Установка

- Клонируйте репозиторий:
```
git clone https://github.com/ArkJzzz/fish_shop.git
```

- Создайте файл ```.env``` и поместите в него токены Telegram и Elastic Path, а так же данные для доступа к Redis:
```
PROD_TELEGRAM_TOKEN=<Ваш токен>
ADMIN_CHAT_ID=<ID чата администратора магазина> (можно узнать, написав сообщение боту @userinfobot)
ELASTICPATH_CLIENT_ID=<Client ID>
REDIS_HOST=<Адрес БД>
REDIS_PORT=<Порт>
REDIS_DB=<Номер БД, по умолчанию 0>
REDIS_PASSWORD=<Пароль>
```

- Установите зависимости:
```
pip3 install -r requirements.txt
```

## Запуск

```
python3 tg-bot.py
```

**Как запускать на сервере:**

- шпаргалка по деплою на [Heroku](https://github.com/ArkJzzz/heroku_deploy)
- шпаргалка по деплою на [удаленном сервере с Ubuntu](https://github.com/ArkJzzz/remote_server_deploy.git)

------
Пример работающего бота-магазина: [@ArkJzzz_fish_shop_bot](https://telegram.me/ArkJzzz_fish_shop_bot)