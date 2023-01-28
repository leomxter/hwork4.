from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import config
import logging
import sqlite3

bot = Bot(token=config.token)
dp = Dispatcher(bot, storage=MemoryStorage())    
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

connect = sqlite3.connect('users.db')
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    id_user INTEGER,
    contact['phone_number'] INTEGER
    );
    """)

connect2 = sqlite3.connect('address.db')
cursor2 = connect2.cursor()
cursor2.execute("""CREATE TABLE IF NOT EXISTS users(
    address_longtitude VARCHAR(255),
    address_latitude VARCHAR(255),
    id_user INTEGER
    );
    """)
connect.commit()

connect3 = sqlite3.connect('orders.db')
cursor3 = connect3.cursor()
cursor3.execute("""CREATE TABLE IF NOT EXISTS users(
    address_destination VARCHAR(255),
    title VARCHAR(255),
    date_time_order INTEGER
    );
    """)
connect.commit()

@dp.message_handler(commands = 'start')
async def start(msg: types.Message):
    inline_kb =[
        [InlineKeyboardButton("Отправить номер", callback_data = "contact")],
        [InlineKeyboardButton("Отправить локацию", callback_data = "location")],
        [InlineKeyboardButton("Заказать", callback_data = "order")]
    ]
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_kb)
    await msg.answer(f"Здраствуйте {msg.from_user.first_name}", reply_markup=inline_keyboard)

class ContactGet(StatesGroup):
    contact = State()

class LocationGet(StatesGroup):
    location = State()

class OrderGet(StatesGroup):
    order = State()

@dp.callback_query_handler(lambda call: call)
async def call(call):
    print(call)
    if call.data == "Отправить номер":
        print('contact')
    await ContactGet.contact.set()
    
@dp.callback_query_handler(lambda call: call)
async def call(call):
    print(call)
    if call.data == "Отправить локацию":
        print('location')
    await LocationGet.location.set()

@dp.callback_query_handler(lambda call: call)
async def call(call):
    print(call)
    if call.data == "Заказать":
        print('order')
    await OrderGet.order.set()

@dp.message_handler(state = ContactGet.contact)
async def UserInfo(message:types.Message, state:FSMContext):
    cursor = connect.cursor()
    cursor.execute(f"SELECT id_user FROM users WHERE id_user = {message.from_user.id};")
    res = cursor.fetchall()
    if res == []:
        cursor.execute(f"""INSERT INTO users VALUES ('{message.from_user.username}', 
        '{message.from_user.first_name}', '{message.from_user.last_name}', 
        {message.from_user.id}, {message.contact['phone_number']}')""")
        await state.finish()
    connect.commit()

dp.message_handler(state = LocationGet.location)
async def UserInfo(message:types.Message, state:FSMContext):
    cursor2 = connect2.cursor()
    cursor2.execute(f"""INSERT INTO users VALUES ('{message.from_user.location['longtitude']}', 
    '{message.from_user.location['latitude']}', {message.from_user.id}')""")
    await state.finish()
    connect2.commit()

dp.message_handler(state = OrderGet.order)
async def UserInfo(message:types.Message, state:FSMContext):
    cursor3 = connect3.cursor()
    cursor3.execute(f"""INSERT INTO users VALUES ('{message.data_time_order}')""")
    await state.finish()
    connect3.commit()

executor.start_polling(dp)