from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes, CallbackQueryHandler

from keyboards import get_professions_keyboard
from database import log_interaction  # Add this import
# Опции стартового капитала
CAPITAL_OPTIONS = [200000, 500000, 1000000]

# Данные для каждого стартового капитала
CAPITAL_DATA = {
    200000: {
        'education': 50000,
        'equipment': 140000,
        'materials': 10000,
        'production': '600-900 г',
        'income_retail': '510,000 - 765,000 ₽',
        'income_wholesale': '360,000 - 540,000 ₽',
        'net_profit_retail': '310,000 - 565,000 ₽',
        'net_profit_wholesale': '160,000 - 340,000 ₽',
        'time_spent': '3-4 месяца',
    },
    500000: {
        'education': 100000,
        'equipment': 380000,
        'materials': 20000,
        'production': '2.5 - 3.75 кг',
        'income_wholesale': '1,500,000 - 2,250,000 ₽',
        'net_profit_wholesale': '1,000,000 - 1,750,000 ₽',
        'time_spent': '3-4 месяца',
    },
    1000000: {
        'education': 100000,
        'equipment': 850000,
        'materials': 50000,
        'production': '6 - 8 кг',
        'income_wholesale': '3,600,000 - 4,800,000 ₽',
        'net_profit_wholesale': '2,600,000 - 3,800,000 ₽',
        'time_spent': '3-4 месяца',
    },
}

# Кнопки калькулятора для Профессии 4
CALCULATOR_BUTTONS_prof4 = [
    [InlineKeyboardButton('Стартовый капитал', callback_data='prof4_calc_edit_capital')],
    [InlineKeyboardButton('Рассчитать', callback_data='prof4_calc_calculate')],
]

# Кнопки результатов калькулятора для Профессии 4
CALCULATOR_RESULT_BUTTONS_prof4 = [
    [InlineKeyboardButton('Вернуться к калькулятору', callback_data='prof4_calc_back')],
    [InlineKeyboardButton('Как начать зарабатывать?', callback_data='prof4_page2')],
    [InlineKeyboardButton('Вернуться к выбору профессии?', callback_data='prof4_back_to_professions')],
    [InlineKeyboardButton('Получить стикерпак  ', url="https://t.me/addstickers/Farmer50")],
]

# Функция для создания сообщения калькулятора
def get_calculator_message_prof4(user_data):
    capital = user_data.get('prof4_capital', 200000)
    capital_info = CAPITAL_DATA[capital]

    message = (
        f"**Выбери подходящий тебе вариант:**\n\n"
        f"💰 *Стартовый капитал:* {capital} ₽\n"
        f"🎓 *Обучение:* {capital_info['education']} ₽\n"
        f"🛠️ *Оборудование:* {capital_info['equipment']} ₽\n"
        f"🧪 *Семена:* {capital_info['materials']} ₽\n"
        f"📦 *Произведено товара:* {capital_info['production']}\n\n"
        f"Используйте кнопку ниже для изменения стартового капитала."
    )
    return message

# Обработчик для Профессии 4
async def handle_profession4_start(query, context: ContextTypes.DEFAULT_TYPE):
    user = query.from_user
    bot_token = context.bot.token

    # Log the interaction
    log_interaction(user.id, bot_token, 'profession4_start', 'Opened grower calculator')
    # Отправляем изображение и текст для Профессии 4
    await query.message.reply_photo(
        photo='https://ninjabox.org/storage/707f2429-4002-426e-b4bd-ee85d4822792/fowj9hs3z1l8rvyn.jpg',
        caption='*Агроном* — узнай все секреты по успешной культивации сельскохозяйственных культур.\n\n'
            '🟩 *Вы получите:*\n\n'
            '🟢 *Образование:* доступ к современным курсам и обновляемым материалам по агротехнике.\n'
            '🟢 *Прямое сотрудничество:* урожай реализуется через партнёрскую сеть, что обеспечивает стабильный сбыт.\n'
            '🟢 *Возможности:* поддержка и инвестиции в развитие вашей фермы и расширение производства.\n'
            '🟢 *Бонусы:* участвуйте в партнёрской программе и получайте вознаграждение за привлечённых участников.\n'
            '🟢 *Статус:* ваш профессионализм будет признан, а профиль отмечен как сертифицированный специалист.\n\n',

        parse_mode='Markdown',
    )

    # Инициализируем значения калькулятора
    context.user_data['prof4_capital'] = 200000  # начальный стартовый капитал

    # Отправляем калькулятор
    calculator_keyboard = InlineKeyboardMarkup(CALCULATOR_BUTTONS_prof4)
    await query.message.reply_text(
        get_calculator_message_prof4(context.user_data),
        reply_markup=calculator_keyboard,
        parse_mode='Markdown',
    )

# Обработчик калькулятора для Профессии 4
async def handle_prof4_calculator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    user = query.from_user
    bot_token = context.bot.token

    if data == 'prof4_calc_edit_capital':
        capital = context.user_data.get('prof4_capital', 200000)
        current_index = CAPITAL_OPTIONS.index(capital)
        next_index = (current_index + 1) % len(CAPITAL_OPTIONS)
        new_capital = CAPITAL_OPTIONS[next_index]
        context.user_data['prof4_capital'] = new_capital
        log_interaction(user.id, bot_token, 'prof4_calc', f'capital_changed: {new_capital}₽')
        await update_calculator_message_prof4(query, context)

    elif data == 'prof4_calc_calculate':
        await calculate_results_prof4(query, context)

    elif data == 'prof4_calc_back':
        log_interaction(user.id, bot_token, 'prof4_navigation', 'back_to_calculator')
        await update_calculator_message_prof4(query, context)

    elif data == 'prof4_page2':
        log_interaction(user.id, bot_token, 'prof4_navigation', 'view_page2')
        await send_prof4_page2(query, context)

    elif data == 'prof4_back_to_professions':
        log_interaction(user.id, bot_token, 'prof4_navigation', 'back_to_professions')
        await query.edit_message_text(
            text="Выберите профессию",
            reply_markup=get_professions_keyboard()
        )

    elif data == 'prof4_no_op':
        # Ничего не делаем
        pass

    else:
        await query.edit_message_text("Неизвестная команда калькулятора.")

# Функция для обновления сообщения калькулятора
async def update_calculator_message_prof4(query, context):
    await query.edit_message_text(
        get_calculator_message_prof4(context.user_data),
        reply_markup=InlineKeyboardMarkup(CALCULATOR_BUTTONS_prof4),
        parse_mode='Markdown',
    )

# Функция для расчёта результатов
async def calculate_results_prof4(query, context):
    user = query.from_user
    bot_token = context.bot.token

    capital = context.user_data.get('prof4_capital', 200000)
    capital_info = CAPITAL_DATA[capital]

    # Формирование сообщения с результатами
    result_message = f"**Результаты расчёта:**\n\n"
    result_message += f"💰 *Стартовый капитал:* {capital} ₽\n"

    # Log the calculation
    log_data = {
        'capital': capital,
        'education_cost': capital_info['education'],
        'equipment_cost': capital_info['equipment'],
        'materials_cost': capital_info['materials'],
        'production': capital_info['production'],
        'time_spent': capital_info['time_spent']
    }

    if capital == 200000:
        result_message += (
            f"💵 *Чистая прибыль (Мини-Опт):* {capital_info['net_profit_retail']}\n"
            f"💵 *Чистая прибыль (Опт):* {capital_info['net_profit_wholesale']}\n"
        )
    else:
        result_message += f"💵 *Чистая прибыль (Опт):* {capital_info['net_profit_wholesale']}\n"

    log_interaction(user.id, bot_token, 'prof4_calculation', str(log_data))

    result_message += f"⏳ *Затраченное время:* {capital_info['time_spent']}\n\n"
    result_message += (f"**В дальнейшем Ваши затраты будут только на семена.**\n"
                       f"С каждым циклом прибыль будет расти из-за роста Ваших навыков.")
    # Отправка результатов с кнопками
    await query.edit_message_text(
        result_message,
        reply_markup=InlineKeyboardMarkup(CALCULATOR_RESULT_BUTTONS_prof4),
        parse_mode='Markdown',
    )

PAGE2_IMAGE_URL = 'https://ninjabox.org/storage/707f2429-4002-426e-b4bd-ee85d4822792/fowj9hs3z1l8rvyn.jpg'
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

async def send_prof4_page2(query, context):
    user = query.from_user
    bot_token = context.bot.token
    log_interaction(user.id, bot_token, 'prof4_page2', 'viewed_instructions')
    # Получаем содержимое страницы 2 из CONTENT
    page2_content = CONTENT['page2']
    await query.message.reply_photo(
        photo=page2_content['image'],
        caption=page2_content['text'],
        reply_markup=InlineKeyboardMarkup(page2_content['buttons']),
        parse_mode='Markdown',
    )
# Функция настройки обработчиков для Профессии 4
def setup_handlers(app):
    # Обработчик калькулятора для Профессии 4
    app.add_handler(CallbackQueryHandler(handle_prof4_calculator, pattern='^prof4_.*$'))
