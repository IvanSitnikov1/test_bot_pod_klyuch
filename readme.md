### Бот для тестового задания
#### Описание
Кнопка 1: текст + ссылка на Яндекс карты (Ленина 1 в любом городе).  
Кнопка 2: текст + ссылка на оплату 2 р.  
Кнопка 3: текст + картинка “img1.jpg”. Преобразуем изображение в multipart/form-data и отправляем в чат, добавив подпись.  
Кнопка 4: получить значение А2 гугл таблички “гугл_табличка”  

Токены доступа сохраняются в config.py:  
TELEGRAM_TOKEN = 'Ваш телеграмм токен для бота'  
YOOMONEY_TOKEN = 'Ваш токен Yoomoney'  
Файл с ключами сервисного аккаунта для доступа к гугл таблицам сохранить как:  
credentials.json  
