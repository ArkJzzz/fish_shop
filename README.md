# fish_shop

Описание проекта


## Подготовка

- **elasticpath**
    
    Зарегистрируйтесь на [elasticpath](https://www.elasticpath.com/).

    Получите [ключи для доступа к API](https://dashboard.elasticpath.com/app).

    ![](elasticpath_keys.png)

    Создайте товары [в каталоге товаров](https://dashboard.elasticpath.com/app/catalogue/products)

    ![](elasticpath_keys.png)


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

- Создайте файл ```.env``` и поместите в него токены Telegram и elasticpath, а так же данные для доступа к Redis:
```
TELEGRAM_TOKEN=<Ваш токен>
ELASTICPATH_STORE_ID=<Store ID>
ELASTICPATH_CLIENT_ID=<Client ID>
ELASTICPATH_CLIENT_TOKEN=<Client secret>
REDIS_HOST=<Адрес БД>
REDIS_PORT=<Порт>
REDIS_DB=<Номер БД, по умолчанию 0>
REDIS_PASSWORD=<Пароль>
```

- Установить зависимости:
```
pip3 install -r requirements.txt
```

## Запуск

```
python3 tg-bot.py
```
![](tg-fish-shop.gif)


------
Примеры работающего магазина: [@ArkJzzz_fish_shop_bot](tg://resolve?domain=ArkJzzz_fish_shop_bot)