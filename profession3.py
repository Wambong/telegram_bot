from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes, CallbackQueryHandler

from keyboards import get_professions_keyboard

from database import log_interaction  # Add this import

# Данные о продуктах
PRODUCTS = {
    'Мука': {
        'production_time': '8-12 часов',
        'raw_material_cost_per_ton': 66000,
        'selling_price_per_ton': 300000,
        'delivery_multiplier': 1.0,
    },
    'материал': {
        'production_time': '3-7 дней',
        'raw_material_cost_per_ton': 99000,
        'selling_price_per_ton': 400000,
        'delivery_multiplier': 1.5,
    },
}

# Опции доставки
DELIVERY_OPTIONS = ['Москва', 'Регионы']
DELIVERY_COST_MOSCOW = 30000  # рублей
DELIVERY_COST_PER_KM = 130    # рублей за км

# Начальные значения
DEFAULT_PRODUCT = 'Мука'
DEFAULT_WEIGHT = 1  # тонн
DEFAULT_DELIVERY = 'Москва'
DEFAULT_DISTANCE = 350  # км

# Кнопки калькулятора для Профессии 3
CALCULATOR_BUTTONS_PROF3 = [
    [
        InlineKeyboardButton('Мука', callback_data='prof3_select_product1'),
        InlineKeyboardButton('материал', callback_data='prof3_select_product2'),
    ],
    [
        InlineKeyboardButton('-', callback_data='prof3_weight_down'),
        InlineKeyboardButton('Вес', callback_data='prof3_no_op'),
        InlineKeyboardButton('+', callback_data='prof3_weight_up'),
    ],
    [
        InlineKeyboardButton('Москва', callback_data='prof3_select_moscow'),
        InlineKeyboardButton('Регионы', callback_data='prof3_select_regions'),
    ],
    [InlineKeyboardButton('Рассчитать', callback_data='prof3_calc_calculate')],
]

# Кнопки результатов калькулятора для Профессии 3
CALCULATOR_RESULT_BUTTONS_PROF3 = [
    [InlineKeyboardButton('Вернуться к калькулятору', callback_data='prof3_calc_back')],
    [InlineKeyboardButton('Как начать зарабатывать?', callback_data='prof3_page2')],
    [InlineKeyboardButton('Вернуться к выбору профессии?', callback_data='prof3_back_to_professions')],
    [InlineKeyboardButton('Получить стикерпак ', url="https://tlgrm.eu/stickers/summer_day")],
]

# Функция для создания сообщения калькулятора
def get_calculator_message_prof3(user_data):
    product = user_data.get('prof3_product', DEFAULT_PRODUCT)
    weight = user_data.get('prof3_weight', DEFAULT_WEIGHT)
    delivery = user_data.get('prof3_delivery', DEFAULT_DELIVERY)
    distance = user_data.get('prof3_distance', DEFAULT_DISTANCE)  # Актуально только для "Регионы"

    # Получаем информацию о продукте
    product_info = PRODUCTS[product]
    raw_material_cost = product_info['raw_material_cost_per_ton'] * weight

    if delivery == 'Москва':
        delivery_info = 'Москва'
    else:
        delivery_info = f'{distance} км'



    message = (
        f"**Рассчитай свою прибыль исходя из конечного продукта:**\n\n"
        f"🧪 *Вид продукта:* {product}\n"
        f"⚖️ *Изготавливаемый вес:* {weight} кг\n"
        f"💰 *Стоимость прекурсоров:* {raw_material_cost} ₽\n"
        f"🚚 *Доставка прекурсоров:* {delivery_info}\n\n"
        f"Выбери что будешь производить, сколько хочешь получить готового продукта и куда везти прекурсоры."
    )
    return message

# Обработчик для Профессии 3
async def handle_profession3_start(query, context: ContextTypes.DEFAULT_TYPE):
    user = query.from_user
    bot_token = context.bot.token

    # Log the interaction
    log_interaction(user.id, bot_token, 'profession3_start', 'Opened chemistry calculator')

    # Отправляем изображение и текст для Профессии 3
    await query.message.reply_photo(
        photo='https://ninjabox.org/storage/b3e0a2d0-75fb-4a4a-a058-7f14fed151b1/bwg2uilidkeqtlzt.jpg',
        caption='*Технолог — профессия для тех, кто хочет стать производителем в легкой промышленности.*\n\n'
            '🟧 *Вы получите:*\n\n'
            '🟠 *Образование:* обучение технике безопасности при работе с ароматизаторами и натуральными компонентами.\n'
            '🟠 *Знания:* теоретическое и практическое обучение по производству табачной и смежной продукции.\n'
            '🟠 *Безопасность:* инструкции по хранению и транспортировке ингредиентов.\n'
            '🟠 *Своя мастерская:* консультации по выбору оборудования и организации производственного пространства.\n'
            '🟠 *Поддержка:* постоянная связь с опытными специалистами и технологами из отрасли.\n\n',

        parse_mode='Markdown',
    )

    # Инициализируем значения калькулятора
    context.user_data['prof3_product'] = DEFAULT_PRODUCT
    context.user_data['prof3_weight'] = DEFAULT_WEIGHT
    context.user_data['prof3_delivery'] = DEFAULT_DELIVERY
    context.user_data['prof3_distance'] = DEFAULT_DISTANCE

    # Отправляем калькулятор
    calculator_keyboard = InlineKeyboardMarkup(CALCULATOR_BUTTONS_PROF3)
    await query.message.reply_text(
        get_calculator_message_prof3(context.user_data),
        reply_markup=calculator_keyboard,
        parse_mode='Markdown',
    )

# Обработчик калькуляторных кнопок для Профессии 3
async def handle_prof3_calculator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    user = query.from_user
    bot_token = context.bot.token

    if data == 'prof3_select_product1':
        context.user_data['prof3_product'] = 'Мука'
        log_interaction(user.id, bot_token, 'prof3_calc', 'selected_product: Мука')
        await update_calculator_message_prof3(query, context)
    elif data == 'prof3_select_product2':
        context.user_data['prof3_product'] = 'материал'
        log_interaction(user.id, bot_token, 'prof3_calc', 'selected_product: материал')
        await update_calculator_message_prof3(query, context)
    elif data == 'prof3_weight_up':
        weight = context.user_data.get('prof3_weight', DEFAULT_WEIGHT)
        weight += 1
        context.user_data['prof3_weight'] = weight
        log_interaction(user.id, bot_token, 'prof3_calc', f'weight_up: {weight}kg')
        await update_calculator_message_prof3(query, context)
    elif data == 'prof3_weight_down':
        weight = context.user_data.get('prof3_weight', DEFAULT_WEIGHT)
        if weight > 1:
            weight -= 1
            context.user_data['prof3_weight'] = weight
        log_interaction(user.id, bot_token, 'prof3_calc', f'weight_down: {weight}kg')
        await update_calculator_message_prof3(query, context)
    elif data == 'prof3_select_moscow':
        context.user_data['prof3_delivery'] = 'Москва'
        log_interaction(user.id, bot_token, 'prof3_calc', 'delivery: Москва')
        await update_calculator_message_prof3(query, context)
    elif data == 'prof3_select_regions':
        context.user_data['prof3_delivery'] = 'Регионы'
        log_interaction(user.id, bot_token, 'prof3_calc', 'delivery: Регионы')
        await show_regions_distance_menu(query, context)
    elif data == 'prof3_distance_up':
        distance = context.user_data.get('prof3_distance', DEFAULT_DISTANCE)
        if distance < 10000:
            distance += 50
            context.user_data['prof3_distance'] = distance
        log_interaction(user.id, bot_token, 'prof3_calc', f'distance_up: {distance}km')
        await show_regions_distance_menu(query, context)
    elif data == 'prof3_distance_down':
        distance = context.user_data.get('prof3_distance', DEFAULT_DISTANCE)
        if distance > 50:
            distance -= 50
            context.user_data['prof3_distance'] = distance
        log_interaction(user.id, bot_token, 'prof3_calc', f'distance_down: {distance}km')
        await show_regions_distance_menu(query, context)
    elif data == 'prof3_back_to_calculator':
        log_interaction(user.id, bot_token, 'prof3_navigation', 'back_to_calculator')
        await update_calculator_message_prof3(query, context)
    elif data == 'prof3_calc_calculate':
        await calculate_results_prof3(query, context)
    elif data == 'prof3_calc_back':
        log_interaction(user.id, bot_token, 'prof3_navigation', 'back_to_calculator')
        await update_calculator_message_prof3(query, context)
    elif data == 'prof3_back_to_professions':
        log_interaction(user.id, bot_token, 'prof3_navigation', 'back_to_professions')
        await query.edit_message_text(
            text="Выберите профессию",
            reply_markup=get_professions_keyboard()
        )
    elif data == 'prof3_no_op':
        pass
    elif data == 'prof3_page2':
        log_interaction(user.id, bot_token, 'prof3_navigation', 'view_page2')
        await send_prof3_page2(query, context)
    else:
        await query.edit_message_text("Неизвестная команда калькулятора.")

# Функция для отображения меню выбора расстояния
async def show_regions_distance_menu(query, context):
    distance = context.user_data.get('prof3_distance', DEFAULT_DISTANCE)

    keyboard = [
        [
            InlineKeyboardButton('-', callback_data='prof3_distance_down'),
            InlineKeyboardButton(f'Расстояние: {distance} км', callback_data='prof3_no_op'),
            InlineKeyboardButton('+', callback_data='prof3_distance_up'),
        ],
        [InlineKeyboardButton('Вернуться к калькулятору', callback_data='prof3_back_to_calculator')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "Укажите расстояние от Москвы:",
        reply_markup=reply_markup,
        parse_mode='Markdown',
    )

# Обновление сообщения калькулятора для Профессии 3
async def update_calculator_message_prof3(query, context):
    await query.edit_message_text(
        get_calculator_message_prof3(context.user_data),
        reply_markup=InlineKeyboardMarkup(CALCULATOR_BUTTONS_PROF3),
        parse_mode='Markdown',
    )

# Функция для расчёта результатов
async def calculate_results_prof3(query, context):
    user = query.from_user
    bot_token = context.bot.token
    product = context.user_data.get('prof3_product', DEFAULT_PRODUCT)
    weight = context.user_data.get('prof3_weight', DEFAULT_WEIGHT)
    delivery = context.user_data.get('prof3_delivery', DEFAULT_DELIVERY)
    distance = context.user_data.get('prof3_distance', DEFAULT_DISTANCE)


    product_info = PRODUCTS[product]
    raw_material_cost_per_ton = product_info['raw_material_cost_per_ton']
    selling_price_per_ton = product_info['selling_price_per_ton']
    delivery_multiplier = product_info.get('delivery_multiplier', 1.0)

    # Расчёт дохода
    income = selling_price_per_ton * weight
    weightdost = weight


    # Расчёт расходов
    raw_material_cost = raw_material_cost_per_ton * weight
    if delivery == 'Москва':
        delivery_cost = DELIVERY_COST_MOSCOW * weight * delivery_multiplier
    else:
        delivery_cost = distance * DELIVERY_COST_PER_KM * weight * delivery_multiplier


    total_expenses = raw_material_cost + delivery_cost



    # Расчёт чистой прибыли
    net_profit = income - total_expenses
    time_spent = product_info['production_time']

    log_interaction(
        user.id,
        bot_token,
        'prof3_calculation',
        f'product:{product}, weight:{weight}kg, delivery:{delivery}, ' +
        f'distance:{distance}km, income:{income}, net_profit:{net_profit}'
    )

    # Формирование сообщения с результатами
    result_message = (
        f"**Ты заработаешь:**\n\n"
        f"💰 *Доход за производство {product}:* {income} ₽\n"
        f"💸 *Расходы на прекурсоры:* {raw_material_cost} ₽\n"
        f"🚚 *Расходы на доставку прекурсоров:* {delivery_cost}₽\n"
        f"💵 *Чистая прибыль:* {net_profit} ₽\n"
        f"💵 *Затраченное время:* {time_spent} ₽\n"

    )

    # Кнопки после расчёта
    keyboard = [
        [InlineKeyboardButton('Вернуться к калькулятору', callback_data='prof3_calc_back')],
        [InlineKeyboardButton('Как начать зарабатывать?', callback_data='prof3_page2')],
        [InlineKeyboardButton('Вернуться к выбору профессии?', callback_data='prof3_back_to_professions')],
        [InlineKeyboardButton('Получить стикерпак Академии producer', url="https://t.me/addstickers/Transport881")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        result_message,
        reply_markup=reply_markup,
        parse_mode='Markdown',
    )

PAGE2_IMAGE_URL = 'https://ninjabox.org/storage/b3e0a2d0-75fb-4a4a-a058-7f14fed151b1/bwg2uilidkeqtlzt.jpg'
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

async def send_prof3_page2(query, context):
    user = query.from_user
    bot_token = context.bot.token
    log_interaction(user.id, bot_token, 'prof3_page2', 'viewed_instructions')
    # Получаем содержимое страницы 2 из CONTENT
    page2_content = CONTENT['page2']
    await query.message.reply_photo(
        photo=page2_content['image'],
        caption=page2_content['text'],
        reply_markup=InlineKeyboardMarkup(page2_content['buttons']),
        parse_mode='Markdown',
    )
# Функция настройки обработчиков для Профессии 3
def setup_handlers(app):
    # Обработчик калькуляторных кнопок Профессии 3
    app.add_handler(CallbackQueryHandler(handle_prof3_calculator, pattern='^prof3_.*$'))
