from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes, CallbackQueryHandler

from keyboards import get_professions_keyboard
from database import log_interaction  # Add this import
# Кнопки Калькулятора для Профессии 1
CALCULATOR_BUTTONS_PROF1 = [
    [
        InlineKeyboardButton('-', callback_data='prof1_calc_units_down'),
        InlineKeyboardButton('Кол-во кладов', callback_data='prof1_calc_no_op'),
        InlineKeyboardButton('+', callback_data='prof1_calc_units_up'),
    ],
    [
        InlineKeyboardButton('-', callback_data='prof1_calc_days_down'),
        InlineKeyboardButton('Кол-во дней', callback_data='prof1_calc_no_op'),
        InlineKeyboardButton('+', callback_data='prof1_calc_days_up'),
    ],
    [InlineKeyboardButton('Вес кладов', callback_data='prof1_calc_edit_weight')],
    [InlineKeyboardButton('Рассчитать', callback_data='prof1_calc_calculate')],
]

# Кнопки Результатов Калькулятора для Профессии 1
CALCULATOR_RESULT_BUTTONS_PROF1 = [
    [InlineKeyboardButton('Вернуться к калькулятору', callback_data='prof1_calc_back')],
    [InlineKeyboardButton('Как начать зарабатывать?', callback_data='prof1_page2')],
    [InlineKeyboardButton('Вернуться к выбору профессии?', callback_data='prof1_back_to_professions')],
    [InlineKeyboardButton('Получить стикерпак courier', url="https://t.me/addstickers/Courier9")],

]


WEIGHT_TO_RATE_PROF1 = {
    1: 1000,
    2: 1050,
    3: 1100,
    5: 1200,
}

# Helper функция для создания сообщения калькулятора
def get_calculator_message_prof1(user_data):
    units = user_data.get('prof1_units_per_day', 10)
    days = user_data.get('prof1_days_per_month', 20)
    weight = user_data.get('prof1_weight', 1)
    weight_options = sorted(WEIGHT_TO_RATE_PROF1.keys())
    current_weight = weight if weight in weight_options else 1

    message = (
        f"🔢 *Кол-во кладов в день:* {units}\n"
        f"📅 *Кол-во рабочих дней в месяц:* {days}\n"
        f"⚖️ *Вес кладов:* {current_weight} г\n\n"
        f"Используйте кнопки ниже для изменения параметров."
    )
    return message

# Обработчик для Профессии 1
async def handle_profession1_start(query, context: ContextTypes.DEFAULT_TYPE):
    user = query.from_user
    bot_token = context.bot.token

    # Log the interaction
    log_interaction(user.id, bot_token, 'profession1_start', 'Opened profession 1 calculator')
    # Отправляем изображение и текст для Профессии 1
    await query.message.reply_photo(
        photo='https://ninjabox.org/storage/de5b125a-c679-49a4-990f-f9618b04ed98/3nnf31pqhtzm952v.jpg',
        caption='*Курьер* - Требующая минимальных вложений профессия.\n\n'
                "⬛ Основные преимущества:\n\n"
                "⚫ Опыт не требуется: мы научим Вас всему что нужно знать что-бы безопасно и много зарабатывать!\n"
                "⚫ Реальный заработок: десять тысяч в час по самому минимальному тарифу!\n"
                "⚫ Бесплатное обучение: вы вносите только минимальный депозит, который будет использован как Ваш залог.\n"
                "⚫ Свободный график: работай когда удобно имено тебе! Никаких обязательных норм и штрафов основаных на них.\n"
                "⚫ Юридическая поддержка: ученики Академии получают доступ к бесплатным консультациям с штатными юристами Blackshisha \n\n"
                "Расчитайте свою ЗП в нашем калькуляторе опираясь на свои возможности! \n",
        parse_mode='Markdown',
    )

    # Инициализируем значения калькулятора
    context.user_data['prof1_units_per_day'] = 10
    context.user_data['prof1_days_per_month'] = 20
    context.user_data['prof1_weight'] = 1  # начальный вес 1 г

    # Отправляем калькулятор
    calculator_keyboard = InlineKeyboardMarkup(CALCULATOR_BUTTONS_PROF1)
    await query.message.reply_text(
        get_calculator_message_prof1(context.user_data),
        reply_markup=calculator_keyboard,
        parse_mode='Markdown',
    )

# Обработчик калькуляторных кнопок для Профессии 1
async def handle_prof1_calculator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    user = query.from_user
    bot_token = context.bot.token

    if data == 'prof1_calc_units_up':
        units = context.user_data.get('prof1_units_per_day', 10)
        if units < 1000:
            units += 1
            context.user_data['prof1_units_per_day'] = units
        log_interaction(user.id, bot_token, 'prof1_calc', f'units_up: {units}')
        await update_calculator_message_prof1(query, context)

    elif data == 'prof1_calc_units_down':
        units = context.user_data.get('prof1_units_per_day', 10)
        if units > 1:
            units -= 1
            context.user_data['prof1_units_per_day'] = units
        log_interaction(user.id, bot_token, 'prof1_calc', f'units_down: {units}')
        await update_calculator_message_prof1(query, context)

    elif data == 'prof1_calc_days_up':
        days = context.user_data.get('prof1_days_per_month', 20)
        if days < 31:
            days += 1
            context.user_data['prof1_days_per_month'] = days
        log_interaction(user.id, bot_token, 'prof1_calc', f'days_up: {days}')
        await update_calculator_message_prof1(query, context)

    elif data == 'prof1_calc_days_down':
        days = context.user_data.get('prof1_days_per_month', 20)
        if days > 1:
            days -= 1
            context.user_data['prof1_days_per_month'] = days
        log_interaction(user.id, bot_token, 'prof1_calc', f'days_down: {days}')
        await update_calculator_message_prof1(query, context)

    elif data == 'prof1_calc_edit_weight':
        weight = context.user_data.get('prof1_weight', 1)
        weight_options = sorted(WEIGHT_TO_RATE_PROF1.keys())
        current_index = weight_options.index(weight) if weight in weight_options else 0
        next_index = (current_index + 1) % len(weight_options)
        new_weight = weight_options[next_index]
        context.user_data['prof1_weight'] = new_weight  # <-- Closing quote added here
        log_interaction(user.id, bot_token, 'prof1_calc', f'weight_change: {new_weight}g')
        await update_calculator_message_prof1(query, context)

    elif data == 'prof1_calc_calculate':
        units = context.user_data.get('prof1_units_per_day', 10)
        days = context.user_data.get('prof1_days_per_month', 20)
        weight = context.user_data.get('prof1_weight', 1)
        rate = WEIGHT_TO_RATE_PROF1.get(weight, 0)

        earn_day = rate * units
        earn_month = earn_day * days
        earn_year = earn_month * 12

        log_interaction(
            user.id,
            bot_token,
            'prof1_calculation',
            f'units:{units}, days:{days}, weight:{weight}g, earn_day:{earn_day}, earn_month:{earn_month}'
        )

        result_message = (
            f"**Результаты расчёта:**\n\n"
            f"💰 *Заработаете за день:* {earn_day} ₽\n"
            f"💰 *Заработаете за месяц:* {earn_month} ₽\n"
            f"💰 *Заработаете за год:* {earn_year} ₽\n"
        )

        await query.edit_message_text(
            result_message,
            reply_markup=InlineKeyboardMarkup(CALCULATOR_RESULT_BUTTONS_PROF1),
            parse_mode='Markdown',
        )

    elif data == 'prof1_calc_back':
        log_interaction(user.id, bot_token, 'prof1_navigation', 'back_to_calculator')
        await query.edit_message_text(
            get_calculator_message_prof1(context.user_data),
            reply_markup=InlineKeyboardMarkup(CALCULATOR_BUTTONS_PROF1),
            parse_mode='Markdown',
        )

    elif data == 'prof1_back_to_professions':
        log_interaction(user.id, bot_token, 'prof1_navigation', 'back_to_professions')
        await query.edit_message_text(
            text="Выберите профессию",
            reply_markup=get_professions_keyboard()
        )

    elif data == 'prof1_calc_no_op':
        # Ничего не делаем
        pass

    elif data == 'prof1_page2':
        # Обработка перехода на страницу 2
        log_interaction(user.id, bot_token, 'prof1_navigation', 'view_page2')
        await send_prof1_page2(query, context)

    else:
        await query.edit_message_text("Неизвестная команда калькулятора.")

# Обновление сообщения калькулятора для Профессии 1
async def update_calculator_message_prof1(query, context):
    await query.edit_message_text(
        get_calculator_message_prof1(context.user_data),
        reply_markup=InlineKeyboardMarkup(CALCULATOR_BUTTONS_PROF1),
        parse_mode='Markdown',
    )
PAGE2_IMAGE_URL = 'https://ninjabox.org/storage/de5b125a-c679-49a4-990f-f9618b04ed98/3nnf31pqhtzm952v.jpg'
CONTENT = {
    'page2': {
        'text':'🥷Начать зарабатывать с Blackshisha просто! \n\n'
                '1. Установи на своё устройство VPN — для защиты своей конфиденциальности и безопасного подключения к интернету.\n\n'
                '2. Зарегистрируйся на blackshisha.com или свяжись с нашей командой через официальный канал, чтобы стать курьером.\n\n'
                '3. Пройди обучение — оно займёт всего несколько дней, а его стоимость полностью компенсируется выдачей товара для начала работы!\n\n'
                ,
        'image': PAGE2_IMAGE_URL,
        'buttons': [
            [InlineKeyboardButton('Что такое VPN и зачем его использовать?', url="https://telegra.ph/What-is-VPN-How-It-Works-Types-of-VPN-07-30/")],
            [InlineKeyboardButton('Что такое Tor Browser.\n\n', url="https://telegra.ph/Tor-Browser---A-Complete-Overview-07-30")],
            [InlineKeyboardButton('Регистрация на К.', url="https://Blackshisha.com")],
            [InlineKeyboardButton('Записаться на обучение', url="https://Blackshisha.com")],
            [InlineKeyboardButton('Написать в поддержку', url="https://t.me/wa_mb")],
        ],
    },
}

async def send_prof1_page2(query, context):
    user = query.from_user
    bot_token = context.bot.token
    log_interaction(user.id, bot_token, 'prof1_page2', 'viewed_instructions')
    # Получаем содержимое страницы 2 из CONTENT
    page2_content = CONTENT['page2']
    await query.message.reply_photo(
        photo=page2_content['image'],
        caption=page2_content['text'],
        reply_markup=InlineKeyboardMarkup(page2_content['buttons']),
        parse_mode='Markdown',
    )


# Функция настройки обработчиков для Профессии 1
def setup_handlers(app):
    # Обработчик калькуляторных кнопок Профессии 1
    app.add_handler(CallbackQueryHandler(handle_prof1_calculator, pattern='^prof1_.*$'))
