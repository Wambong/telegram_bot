from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes, CallbackQueryHandler

from keyboards import get_professions_keyboard
from database import log_interaction  # Add this import

# Кнопки Калькулятора для Профессии 2
CALCULATOR_BUTTONS_PROF2 = [
    [
        InlineKeyboardButton('-', callback_data='prof2_calc_total_weight_down'),
        InlineKeyboardButton('Общий вес', callback_data='prof2_calc_no_op'),
        InlineKeyboardButton('+', callback_data='prof2_calc_total_weight_up'),
    ],
    [
        InlineKeyboardButton('-', callback_data='prof2_calc_distance_down'),
        InlineKeyboardButton('Расстояние', callback_data='prof2_calc_no_op'),
        InlineKeyboardButton('+', callback_data='prof2_calc_distance_up'),
    ],
    [
        InlineKeyboardButton('-', callback_data='prof2_calc_units_down'),
        InlineKeyboardButton('Кол-во заказов', callback_data='prof2_calc_no_op'),
        InlineKeyboardButton('+', callback_data='prof2_calc_units_up'),
    ],
    [InlineKeyboardButton('Изменить вес заказов', callback_data='prof2_calc_edit_order_weight')],
    [InlineKeyboardButton('Рассчитать', callback_data='prof2_calc_calculate')],
]

# Кнопки Результатов Калькулятора для Профессии 2
CALCULATOR_RESULT_BUTTONS_PROF2 = [
    [InlineKeyboardButton('Вернуться к калькулятору', callback_data='prof2_calc_back')],
    [InlineKeyboardButton('Как начать зарабатывать?', callback_data='prof2_page2')],
    [InlineKeyboardButton('Вернуться к выбору профессии?', callback_data='prof2_back_to_professions')],
    [InlineKeyboardButton('Получить стикерпак transport', url="https://t.me/addstickers/Transport881")],
]

# Опции веса заказов и их стоимость
ORDER_WEIGHT_OPTIONS = [
    'от 5 до 10 г',
    'от 11 до 25 г',
    'от 26 до 100 г',
    'от 101 до 250 г',
    'от 251 до 500 г',
    'от 501 до 1000 г',
]

ORDER_WEIGHT_COSTS = {
    'от 5 до 10 г': 1000,
    'от 11 до 25 г': 1600,
    'от 26 до 100 г': 2500,
    'от 101 до 250 г': 5000,
    'от 251 до 500 г': 10000,
    'от 501 до 1000 г': 20000,
}

# Helper функция для создания сообщения калькулятора
def get_calculator_message_prof2(user_data):
    total_weight = user_data.get('prof2_total_weight', 5)
    distance = user_data.get('prof2_distance', 1500)
    units = user_data.get('prof2_units', 10)
    order_weight = user_data.get('prof2_order_weight', 'от 50 до 109 г')

    message = (
        f"**Рассчитай свою прибыль, расходы мы берём на себя!:**\n\n"
        f"⚖️ *Перевозимый вес:* {total_weight} кг\n"
        f"📍 *Расстояние:* {distance} км\n"
        f"🔢 *Кол-во кладов:* {units}\n"
        f"⚖️ *Вес кладов:* {order_weight}\n\n"
        f"Используйте кнопки ниже для изменения параметров."
    )
    return message

# Обработчик для Профессии 2
async def handle_profession2_start(query, context: ContextTypes.DEFAULT_TYPE):
    user = query.from_user
    bot_token = context.bot.token

    # Log the interaction
    log_interaction(user.id, bot_token, 'profession2_start', 'Opened profession 2 calculator')

    # Отправляем изображение и текст для Профессии 2
    await query.message.reply_photo(
        photo='https://ninjabox.org/storage/1b6f0404-b73c-4580-aa51-1d84d86b9534/o4f4ww4zr4kclevt.jpg',
        caption='*Академия Перевозчиков — для тех, кто хочет зарабатывать, путешествуя по всей стране!*\n\n'
                '🟦 *Основные преимущества:*\n\n'
                '🔵 *Эффективность:* быстрое и доступное обучение для старта в профессии логиста или курьера с нуля, а также как курс повышения квалификации.\n'
                '🔵 *Прибыльность:* высокий доход с каждого маршрута! Ваш заработок зависит от объёма доставок и ваших усилий.\n'
                '🔵 *Знания:* всё о безопасности на маршрутах, работе с грузами, документообороте и клиентах. Получи понимание логистических процессов и эффективной работы.\n\n'
                '🔵 *Бесплатное обучение:* стоимость курса полностью засчитывается в виде бонуса или скидки на первое трудоустройство.\n'
                '🔵 *Статус:* успешно прошедшие обучение получают статус выпускника Академии с сертификатом и доступом к внутренним предложениям.\n'
                '🔵 *Образование:* постоянный доступ к обновлённым учебным материалам и поддержке сообщества.\n',

        parse_mode='Markdown',
    )

    # Инициализируем значения калькулятора
    context.user_data['prof2_total_weight'] = 5  # начальный общий вес
    context.user_data['prof2_distance'] = 1500  # начальное расстояние в км
    context.user_data['prof2_units'] = 10  # начальное количество заказов
    context.user_data['prof2_order_weight'] = 'от 251 до 500 г'  # начальный вес заказов

    # Отправляем калькулятор
    calculator_keyboard = InlineKeyboardMarkup(CALCULATOR_BUTTONS_PROF2)
    await query.message.reply_text(
        get_calculator_message_prof2(context.user_data),
        reply_markup=calculator_keyboard,
        parse_mode='Markdown',
    )

# Обработчик калькуляторных кнопок для Профессии 2
async def handle_prof2_calculator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    user = query.from_user
    bot_token = context.bot.token

    if data == 'prof2_calc_total_weight_up':
        total_weight = context.user_data.get('prof2_total_weight', 5)
        if total_weight < 1000:  # Максимальный общий вес
            total_weight += 1
            context.user_data['prof2_total_weight'] = total_weight

        log_interaction(user.id, bot_token, 'prof2_calc', f'total_weight_up: {total_weight}kg')
        await update_calculator_message_prof2(query, context)

    elif data == 'prof2_calc_total_weight_down':
        total_weight = context.user_data.get('prof2_total_weight', 5)
        if total_weight > 1:  # Минимальный общий вес
            total_weight -= 1
            context.user_data['prof2_total_weight'] = total_weight
        log_interaction(user.id, bot_token, 'prof2_calc', f'total_weight_down: {total_weight}kg')
        await update_calculator_message_prof2(query, context)

    elif data == 'prof2_calc_distance_up':
        distance = context.user_data.get('prof2_distance', 1500)
        if distance < 10000:  # Максимальное расстояние
            distance += 100
            context.user_data['prof2_distance'] = distance
        log_interaction(user.id, bot_token, 'prof2_calc', f'distance_up: {distance}km')
        await update_calculator_message_prof2(query, context)

    elif data == 'prof2_calc_distance_down':
        distance = context.user_data.get('prof2_distance', 1500)
        if distance > 100:  # Минимальное расстояние
            distance -= 100
            context.user_data['prof2_distance'] = distance
        log_interaction(user.id, bot_token, 'prof2_calc', f'distance_down: {distance}km')
        await update_calculator_message_prof2(query, context)

    elif data == 'prof2_calc_units_up':
        units = context.user_data.get('prof2_units', 10)
        if units < 1000:
            units += 1
            context.user_data['prof2_units'] = units
        log_interaction(user.id, bot_token, 'prof2_calc', f'units_up: {units}')
        await update_calculator_message_prof2(query, context)

    elif data == 'prof2_calc_units_down':
        units = context.user_data.get('prof2_units', 10)
        if units > 1:
            units -= 1
            context.user_data['prof2_units'] = units
        log_interaction(user.id, bot_token, 'prof2_calc', f'units_down: {units}')
        await update_calculator_message_prof2(query, context)

    elif data == 'prof2_calc_edit_order_weight':
        order_weight = context.user_data.get('prof2_order_weight', 'от 50 до 109 кг')
        current_index = ORDER_WEIGHT_OPTIONS.index(order_weight)
        next_index = (current_index + 1) % len(ORDER_WEIGHT_OPTIONS)
        new_order_weight = ORDER_WEIGHT_OPTIONS[next_index]
        context.user_data['prof2_order_weight'] = new_order_weight
        log_interaction(user.id, bot_token, 'prof2_calc', f'weight_change: {new_order_weight}')
        await update_calculator_message_prof2(query, context)

    elif data == 'prof2_calc_calculate':
        total_weight = context.user_data.get('prof2_total_weight', 5)
        distance = context.user_data.get('prof2_distance', 1500)
        units = context.user_data.get('prof2_units', 10)
        order_weight = context.user_data.get('prof2_order_weight', 'от 50 до 109 кг')

        # Рассчитываем оплату за общий вес
        payment_total_weight = 80 * distance * total_weight

        # Рассчитываем оплату за заказы
        order_weight_cost = ORDER_WEIGHT_COSTS.get(order_weight, 0)
        payment_orders = units * order_weight_cost
        payment_all = payment_orders + payment_total_weight

        # Рассчитываем потраченное время
        time_spent_hours = (distance / 100) * 2
        time_spent_hours = int(round(time_spent_hours))  # Округляем до целого числа

        # Log the calculation
        log_interaction(
            user.id,
            bot_token,
            'prof2_calculation',
            f'total_weight:{total_weight}kg, distance:{distance}km, units:{units}, ' +
            f'order_weight:{order_weight}, total_payment:{payment_all}₽'
        )

        result_message = (
            f"**Результаты расчёта:**\n\n"
            f"💰 *Оплата за перевозимый вес:* {payment_total_weight:.2f} ₽\n"
            f"💰 *Оплата за клады:* {payment_orders} ₽\n"
            f"💰 *Всего заработаете за рейс:* {payment_all} ₽\n"
            f"⏰ *Время затраченное на рейс:~* {time_spent_hours} ч.\n"
            f" *Компенсируем расходы на топливо, еду и жильё*\n"

        )

        await query.edit_message_text(
            result_message,
            reply_markup=InlineKeyboardMarkup(CALCULATOR_RESULT_BUTTONS_PROF2),
            parse_mode='Markdown',
        )

    elif data == 'prof2_calc_back':
        log_interaction(user.id, bot_token, 'prof2_navigation', 'back_to_calculator')
        await query.edit_message_text(
            get_calculator_message_prof2(context.user_data),
            reply_markup=InlineKeyboardMarkup(CALCULATOR_BUTTONS_PROF2),
            parse_mode='Markdown',
        )

    elif data == 'prof2_back_to_professions':
        log_interaction(user.id, bot_token, 'prof2_navigation', 'back_to_professions')
        await query.edit_message_text(
            text="Выберите профессию",
            reply_markup=get_professions_keyboard()
        )
    elif data == 'prof2_calc_no_op':
        # Ничего не делаем
        pass

    elif data == 'prof2_page2':
        log_interaction(user.id, bot_token, 'prof2_navigation', 'view_page2')
        # Обработка перехода на страницу 2
        await send_prof2_page2(query, context)

    else:
        await query.edit_message_text("Неизвестная команда калькулятора.")

# Обновление сообщения калькулятора для Профессии 2
async def update_calculator_message_prof2(query, context):
    await query.edit_message_text(
        get_calculator_message_prof2(context.user_data),
        reply_markup=InlineKeyboardMarkup(CALCULATOR_BUTTONS_PROF2),
        parse_mode='Markdown',
    )

PAGE2_IMAGE_URL = 'https://ninjabox.org/storage/de5b125a-c679-49a4-990f-f9618b04ed98/3nnf31pqhtzm952v.jpg'
CONTENT = {
    'page2': {
        'text': '🥷Начать зарабатывать с Blackshisha, просто! \n\n'
                '1. Установи на своё устройство VPN — для защиты своей конфиденциальности и безопасного подключения к интернету.\n\n'
                '2. Зарегистрируйся на blackshisha.com или свяжись с нашей командой через официальный канал, чтобы стать курьером.\n\n'
                '3. Пройди обучение — оно займёт всего несколько дней, а его стоимость полностью компенсируется выдачей товара для начала работы!\n\n'
                ,
        'image': PAGE2_IMAGE_URL,
        'buttons': [
            [InlineKeyboardButton('Что такое VPN и зачем его использовать?', url="https://telegra.ph/What-is-VPN-How-It-Works-Types-of-VPN-07-30")],
            [InlineKeyboardButton('Что такое Tor Browser.\n\n', url="https://telegra.ph/Tor-Browser---A-Complete-Overview-07-30")],
            [InlineKeyboardButton('Регистрация на К.', url="https://Blackshisha.com")],
            [InlineKeyboardButton('Записаться на обучение', url="https://Blackshisha.com")],
            [InlineKeyboardButton('Написать в поддержку', url="https://t.me/wa_mb")],
        ],
    },
}

async def send_prof2_page2(query, context):

    user = query.from_user
    bot_token = context.bot.token
    log_interaction(user.id, bot_token, 'prof2_page2', 'viewed_instructions')

    # Получаем содержимое страницы 2 из CONTENT
    page2_content = CONTENT['page2']
    await query.message.reply_photo(
        photo=page2_content['image'],
        caption=page2_content['text'],
        reply_markup=InlineKeyboardMarkup(page2_content['buttons']),
        parse_mode='Markdown',
    )

# Функция настройки обработчиков для Профессии 2
def setup_handlers(app):
    # Обработчик калькуляторных кнопок Профессии 2
    app.add_handler(CallbackQueryHandler(handle_prof2_calculator, pattern='^prof2_.*$'))
