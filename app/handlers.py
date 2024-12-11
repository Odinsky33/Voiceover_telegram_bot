from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, BufferedInputFile
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from gtts import gTTS
from io import BytesIO
import uuid


router = Router()


class Handler(StatesGroup):
    selecting_language = State()
    selected_ru_language = State()
    selected_en_language = State()
    write_text = State()
    writening_text = State()



@router.message(CommandStart())
async def echo(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name} рад тебя видеть!\n/change_language - озвучить текст\n/write_text - тест")



@router.message(Command("change_language"))
async def change_language(message: Message, state: FSMContext):
    kb_list = [
        [KeyboardButton(text="ru"), KeyboardButton(text="en")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    await message.answer("Выберите язык, на котором будет написан ваш текст", reply_markup=keyboard, resize_keyboard=True)
    await state.set_state(Handler.selecting_language)


@router.message(F.text.lower()=="ru")
async def ru_language(message: Message, state: FSMContext):
    await message.reply("Выбрана озвучка на русском")
    await state.set_state(Handler.selected_ru_language)
    await message.answer("Введите ваш текст")

@router.message(F.text.lower()=="en")
async def en_language(message: Message, state: FSMContext):
    await message.reply("Selected english language")
    await state.set_state(Handler.selected_en_language)
    await message.answer("Write your text")


@router.message(Handler.selected_ru_language)
async def ru_text(message: Message, state: FSMContext):
    myobj = gTTS(text=message.text, lang="ru", slow=False)
    audio = BytesIO()
    myobj.write_to_fp(audio)
    audio_file = BufferedInputFile(audio.getvalue(), filename=str(uuid.uuid1()))
    await message.reply_voice(audio_file)
    await state.set_state(Handler.selected_ru_language)


@router.message(Handler.selected_en_language)
async def en_text(message: Message, state: FSMContext):
    myobj = gTTS(text=message.text, lang="en", slow=False)
    audio = BytesIO()
    myobj.write_to_fp(audio)
    audio_file = BufferedInputFile(audio.getvalue(), filename=str(uuid.uuid1()))
    await message.reply_voice(audio_file)
    await state.set_state(Handler.selected_en_language)

@router.message(Handler.writening_text)
async def write_text(message: Message, state: FSMContext):
    kb_list = [
        [KeyboardButton(text="ru"), KeyboardButton(text="en")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    await message.answer("Выберите язык, на котором будет написан ваш текст", reply_markup=keyboard,
                         resize_keyboard=True)
    if F.text.lower() == "ru":
        await message.reply("Выбрана озвучка на русском")
        await state.set_state(Handler.selected_ru_language)
        await message.answer("Введите ваш текст")
        await ru_text()
    if F.text.lower() == "en":
        await message.reply("Selected english language")
        await state.set_state(Handler.selected_en_language)
        await message.answer("Write your text")
        await en_text()
