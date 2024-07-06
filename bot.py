import asyncio
import os
import logging
from datetime import datetime
from uuid import uuid4

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import gspread
from yoomoney import Client, Quickpay

from config import TELEGRAM_TOKEN, YOOMONEY_TOKEN

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=TELEGRAM_TOKEN)
# Диспетчер
dp = Dispatcher()
# инициализация объектов для работы с Google Sheets
gc = gspread.service_account(filename='credentials.json')
wks = gc.open("гугл_табличка").sheet1


# Хэндлер на команду /start
@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    # создаем кнопки для клавиатуры
    # при нажатии кнопки отправляется команда в чат
    keyboard = [
        [types.KeyboardButton(text='Кнопка 1')],
        [types.KeyboardButton(text='Кнопка 2')],
        [types.KeyboardButton(text='Кнопка 3')],
        [types.KeyboardButton(text='Кнопка 4')],
    ]

    # создаем клавиатуру и добавляем её на экран
    main_kb = types.ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
    )
    await message.answer('Привет! Нажмите любую кнопку!',
                         reply_markup=main_kb)


# Хэндлер на прочие сообщения
@dp.message()
async def massage_handler(message: types.Message):
    # выполняем проверку на то, какая отправлена команда
    if message.text == 'Кнопка 1':
        # Кнопка 1: текст + ссылка на Яндекс карты (Ленина 1 в любом городе).
        await message.answer('Местоположение Ленина 1А в городе Ярославль')
        await message.answer('https://yandex.ru/maps/16/yaroslavl/house/'
                             'prospekt_lenina_1a/Z0AYfg9jT0IGQFttfXp1cn1qYg==/'
                             '?ll=39.883672%2C57.643196&z=17.05')

    elif message.text == 'Кнопка 2':
        # Кнопка 2: текст + ссылка на оплату 2 р.
        await message.answer('Произведите оплату')

        # создаем форму платежа с данными о переводе
        # используем label как метку конкретного перевода
        label = str(uuid4())
        qp = Quickpay(
            receiver="4100118741122722",
            quickpay_form="shop",
            targets="Sponsor this project",
            paymentType="SB",
            sum=2,
            label=label,
        )

        # отправляем в чат ссылку для оплаты
        await message.answer(qp.redirected_url)

        async def check_payment_status():
            """Функция проверки совершения платежа. Каждые 5с проверяет статус
            платежа с предоставленной меткой"""
            client = Client(YOOMONEY_TOKEN)
            while True:
                await asyncio.sleep(5)
                history = client.operation_history(label=label)
                for operation in history.operations:
                    if operation.status == 'success':
                        return True

        # при подтверждения операции оплаты отправляем сообщение в чат
        if await check_payment_status():
            await message.answer('Платеж выполнен!')

    elif message.text == 'Кнопка 3':
        # Кнопка 3: текст + картинка “img1.jpg”.
        # преобразуем изображение в multipart/form-data и отправляем в чат, добавив подпись
        img_path = os.path.abspath('992.jpg')
        img_file = types.FSInputFile(img_path)
        await message.answer_photo(img_file, caption='Фото паука')

    elif message.text == 'Кнопка 4':
        # Кнопка 4: получить значение А2 гугл таблички “гугл_табличка”
        await message.answer(f'Значение А2 гугл таблички "гугл_табличка": '
                             f'"{wks.acell('A2').value}"')

    else:
        # обрабатываем ввод текста, задаем ожидаемые форматы даты
        date_formats = ['%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y']
        date = ''
        # проверяем сообщение на возможность преобразовать к дате
        for date_format in date_formats:
            try:
                date = datetime.strptime(message.text, date_format)
                break
            except ValueError:
                continue
        # в случае успеха заносим дату в таблицу в столбец "B" в новую строку
        if date:
            row_count = len(wks.col_values(2)) + 1
            wks.update_cell(row_count, 2, message.text)
            await message.answer('Дата верна')
        else:
            await message.answer(
                'Дата не верна, введите дату в одном из следующих форматов: '
                'YYYY-MM-DD, DD.MM.YYYY, DD/MM/YYYY.'
            )


# Запуск процесса пуллинга новых обновлений
async def main():
    await dp.start_polling(bot)


# запуск бота
if __name__ == "__main__":
    asyncio.run(main())
