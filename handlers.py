from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import CommandStart, Command
import keyboards as kb
from excel import schedule_1sm, schedule_2sm, ALLOWED_GRADES
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from database import init_db, add_or_change
from states import Registration, Registration_change
from aiogram.types import FSInputFile
from keyboards import Cm1
from aiogram.types import FSInputFile
from excel import first_grades, second_grades
from database import get_user_grade_from_db, get_user_grade_by_id
import datetime
from aiogram import F, types
user = Router()


@user.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer('''Добро пожаловать!
Это бот с расписанием Школы №11
Создан @lapihhh специально для учеников и учителей 🩷🩷
''', reply_markup=kb.menu)
    await state.set_state(Registration.waiting_for_grade)

async def is_correct_grade(grade, message):
    if grade not in ALLOWED_GRADES:
        await message.answer(
            f"Вы ввели '{grade}', но такого класса нет в системе\n"
            f"Пожалуйста, выберите класс на клавиатуре:"
        )
        return False
    return True


@user.message(Registration.waiting_for_grade)
async def process_grade(message: types.Message, state: FSMContext):
    grade = message.text.strip().upper()
    if grade not in ALLOWED_GRADES:
        await message.answer(
            f"Вы ввели '{grade}', но такого класса нет в системе\n"
            f"Пожалуйста, выберите класс на клавиатуре:"
        )
        return
    add_or_change(message.from_user.id, message.from_user.username or "nn", grade)
    await message.answer(f"Отлично! Теперь ты в {grade} классе", reply_markup=kb.menu_rell)
    await state.clear() # Очищаем состояние


@user.message(Command('chance_class'))
async def cmd_chance_class(message: types.Message, state: FSMContext):
    await message.answer('''Ты хочешь изменить свой класс?
Выбери класс расписание которого ты хочешь получать''', reply_markup=kb.menu)
    await state.set_state(Registration_change.waiting_for_grade_change) 


@user.message(Command('schedule'))
async def cmd_schedule(message: Message):
    await message.answer('Выбери класс, расписание которого ты хочешь посмотреть', reply_markup=kb.menu)
      

@user.message(Command('help'))
async def cmd_schedule(message: Message):
    await message.answer('''Функционал бота:

•  /start — Запускает бота. При повторном использовании этой команды ваши данные будут обновлены в базе данных
•  /schedule — Позволяет просмотреть расписание на неделю для любого класса. При этом ваше текущее расписание остается неизменным, и вы продолжите получать уведомления от своего класса
•  /change_class — Изменяет ваш текущий класс. Ваши остальные данные сохраняются, меняется только привязка к классу

Интерактивные кнопки:

•  'На сегодня' — Показывает расписание вашего класса на текущий день
•  'На завтра' — Показывает расписание вашего класса на следующий день
•  'На неделю' — Показывает расписание вашего класса на всю неделю

Уведомления о расписании:

Бот автоматически отправляет расписание на следующий день:
•  Каждый день (например, в понедельник — на вторник)
•  Для 1-й смены — в 14:00
•  Для 2-й смены — в 18:00
•  По воскресеньям всем пользователям расписание на понедельник отправляется в 17:00
''')


@user.message(F.text == "на сегодня")
async def get_today_schedule(message: types.Message):
    user_id = message.from_user.id
    grade = get_user_grade_from_db(user_id) 
    
    if not grade:
        await message.answer("Класс не выбран. Используйте кнопку 'выбрать класс'")
        return

    today = datetime.datetime.now().isoweekday()

    if grade in first_grades:
        result = schedule_1sm(grade, today)
    elif grade in second_grades:
        result = schedule_2sm(grade, today)
    else:
        result = "Ошибка: класс не найден в списках смен"

    await message.answer(result)

@user.message(F.text == "на завтра")
async def get_tomorrow_schedule(message: types.Message):
    user_id = message.from_user.id
    grade = get_user_grade_from_db(user_id)
    
    if not grade:
        await message.answer("Класс не выбран")
        return

    tomorrow = datetime.datetime.now().isoweekday() + 1
    if tomorrow > 7: 
        tomorrow = 1

    if grade in first_grades:
        result = schedule_1sm(grade, tomorrow)
    elif grade in second_grades:
        result = schedule_2sm(grade, tomorrow)
    else:
        result = "Ошибка в базе данных"

    await message.answer(result)

@user.message(F.text == 'на неделю')
async def get_full_week_schedule(message: types.Message):
    grade = get_user_grade_from_db(message.from_user.id)
    
    if not grade:
        await message.answer("Вы не выбрали класс! Нажмите 'выбрать класс'")
        return

    week_text = f"Расписание на неделю для {grade}:\n\n"

    for day in range(1, 6):
        if grade in first_grades:
            day_schedule = schedule_1sm(grade, day)
        elif grade in second_grades:
            day_schedule = schedule_2sm(grade, day)
        else:
            day_schedule = "Класс не найден в списках смен"
        
        week_text += f"{day_schedule}\n"

    await message.answer(week_text)

@user.message(Command('chance_class'))
async def cmd_chance_class(message: types.Message, state: FSMContext):
    await message.answer('''Ты хочешь изменить свой класс?
Тогда выбери класс расписание которого ты хочешь получать''', reply_markup=kb.menu)
    await state.set_state(Registration_change.waiting_for_grade_change)
 
@user.message(Registration_change.waiting_for_grade_change)
async def process_grade(message: types.Message, state: FSMContext):
    grade = message.text 
    user_id = message.from_user.id
    username = message.from_user.username or "NoName"
    if grade not in ALLOWED_GRADES:
        await message.answer(
            f"Вы ввели '{grade}', но такого класса нет в системе\n"
            f"Пожалуйста, выберите класс на клавиатуре:"
        )
        return
    add_or_change(message.from_user.id, message.from_user.username or "nn", grade)
    await state.clear() 
    await message.answer(f"Теперь ты из {grade} класса. Тебе будет присылаться расписание именно этого класса каждый день ", reply_markup=kb.menu_rell )
    await state.clear()
    
    
    
@user.message(F.text == '5А')
async def cmd_hello(message: Message):
    await message.answer('''Ты выбрал класс - 5А
Выберите расписание на день''',
                         reply_markup=kb.FiveA)

@user.callback_query(F.data == 'Понедельник5a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("5А",1))

@user.callback_query(F.data == 'Вторник5a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("5А",2))

@user.callback_query(F.data == 'Среда5a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("5А",3))
    
@user.callback_query(F.data == 'Четверг5a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("5А",4))

@user.callback_query(F.data == 'Пятница5a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("5А",5))


@user.message(F.text == '5Б')
async def cmd_hello(message: Message):
    await message.answer('''Ты выбрал класс - 5Б
Выберите расписание на день''',
                         reply_markup=kb.FiveB)

@user.callback_query(F.data == 'Понедельник5b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("5Б",1))

@user.callback_query(F.data == 'Вторник5b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("5Б",2))

@user.callback_query(F.data == 'Среда5b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("5Б",3))
    
@user.callback_query(F.data == 'Четверг5b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("5Б",4))

@user.callback_query(F.data == 'Пятница5b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("5Б",5))



@user.message(F.text == '5В')
async def cmd_hello(message: Message):
    await message.answer('''Ты выбрал класс - 5В
Выбери расписание на день''',
                         reply_markup=kb.FiveV)

@user.callback_query(F.data == 'Понедельник5v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("5В",1))

@user.callback_query(F.data == 'Вторник5v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("5В",2))

@user.callback_query(F.data == 'Среда5v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("5В",3))
    
@user.callback_query(F.data == 'Четверг5v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("5В",4))

@user.callback_query(F.data == 'Пятница5v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("5В",5))



@user.message(F.text == '6А')
async def cmd_hello(message: Message):
    await message.answer('''Ты выбрал класс - 6А
Выбери расписание на день''',
                         reply_markup=kb.SixA)

@user.callback_query(F.data == 'Понедельник6a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("6А",1))

@user.callback_query(F.data == 'Вторник6a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("6А",2))

@user.callback_query(F.data == 'Среда6a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("6А",3))
    
@user.callback_query(F.data == 'Четверг6a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("6А",4))

@user.callback_query(F.data == 'Пятница6a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("6А",5))


@user.message(F.text == '6Б')
async def cmd_hello(message: Message):
    await message.answer('''Ты выбрал класс - 6Б
Выбери расписание на день''',
                         reply_markup=kb.SixB)

@user.callback_query(F.data == 'Понедельник6b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("6Б",1))

@user.callback_query(F.data == 'Вторник6b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("6Б",2))

@user.callback_query(F.data == 'Среда6b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("6Б",3))
    
@user.callback_query(F.data == 'Четверг6b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("6Б",4))

@user.callback_query(F.data == 'Пятница6b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("6Б",5))


@user.message(F.text == '6В')
async def cmd_hello(message: Message):
    await message.answer('''Ты выбрал класс - 6В
Выбери расписание на день''',
                         reply_markup=kb.SixV)

@user.callback_query(F.data == 'Понедельник6v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("6В",1))

@user.callback_query(F.data == 'Вторник6v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("6В",2))

@user.callback_query(F.data == 'Среда6v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("6В",3))
    
@user.callback_query(F.data == 'Четверг6v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("6В",4))

@user.callback_query(F.data == 'Пятница6v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("6В",5))



@user.message(F.text == '7А')
async def cmd_hello(message: Message):
    await message.answer('''Ты выбрал класс - 7А
Выбери расписание на день''',
                         reply_markup=kb.SevenA)

@user.callback_query(F.data == 'Понедельник7a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("7А",1))

@user.callback_query(F.data == 'Вторник7a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("7А",2))

@user.callback_query(F.data == 'Среда7a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("7А",3))
    
@user.callback_query(F.data == 'Четверг7a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("7А",4))

@user.callback_query(F.data == 'Пятница7a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("7А",5))


@user.message(F.text == '7Б')
async def cmd_hello(message: Message):
    await message.answer('''Ты выбрал класс - 7Б
Выбери расписание на день''',
                         reply_markup=kb.SevenB)

@user.callback_query(F.data == 'Понедельник7b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("7Б", 1))

@user.callback_query(F.data == 'Вторник7b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("7Б", 2))

@user.callback_query(F.data == 'Среда7b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("7Б", 3))
    
@user.callback_query(F.data == 'Четверг7b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("7Б", 4))

@user.callback_query(F.data == 'Пятница7b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("7Б", 5))


@user.message(F.text == '7В')
async def cmd_hello(message: Message):
    await message.answer('''Ты выбрал класс - 7В
Выбери расписание на день''',
                         reply_markup=kb.SevenV)

@user.callback_query(F.data == 'Понедельник7v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("7В", 1))

@user.callback_query(F.data == 'Вторник7v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("7В", 2))

@user.callback_query(F.data == 'Среда7v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("7В", 3))
    
@user.callback_query(F.data == 'Четверг7v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("7В", 4))

@user.callback_query(F.data == 'Пятница7v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("7В", 5))



@user.message(F.text == '8А')
async def cmd_hello(message: Message):
    await message.answer('''Ты выбрал класс - 8А
Выбери расписание на день''',
                         reply_markup=kb.EightA)

@user.callback_query(F.data == 'Понедельник8a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("8А", 1))

@user.callback_query(F.data == 'Вторник8a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("8А", 2))

@user.callback_query(F.data == 'Среда8a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("8А", 3))
    
@user.callback_query(F.data == 'Четверг8a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("8А", 4))

@user.callback_query(F.data == 'Пятница8a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("8А", 5))


@user.message(F.text == '8Б')
async def cmd_hello(message: Message):
    await message.answer('''Ты выбрал класс - 8Б
Выбери расписание на день''',
                         reply_markup=kb.EightB)

@user.callback_query(F.data == 'Понедельник8b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("8Б", 1))

@user.callback_query(F.data == 'Вторник8b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("8Б", 2))

@user.callback_query(F.data == 'Среда8b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("8Б", 3))
    
@user.callback_query(F.data == 'Четверг8b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("8Б", 4))

@user.callback_query(F.data == 'Пятница8b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("8Б", 5))


@user.message(F.text == '8В')
async def cmd_hello(message: Message):
    await message.answer('''Ты выбрал класс - 8В
Выбери расписание на день''',
                         reply_markup=kb.EightV)

@user.callback_query(F.data == 'Понедельник8v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("8В", 1))

@user.callback_query(F.data == 'Вторник8v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("8В", 2))

@user.callback_query(F.data == 'Среда8v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("8В", 3))
    
@user.callback_query(F.data == 'Четверг8v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("8В", 4))

@user.callback_query(F.data == 'Пятница8v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_2sm("8В", 5))



@user.message(F.text == '9А')
async def cmd_hello(message: Message):
    await message.answer('''Ты выбрал класс - 9А
Выбери расписание на день''',
                         reply_markup=kb.NineA)

@user.callback_query(F.data == 'Понедельник9a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("9А", 1))

@user.callback_query(F.data == 'Вторник9a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("9А", 2))

@user.callback_query(F.data == 'Среда9a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("9А", 3))
    
@user.callback_query(F.data == 'Четверг9a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("9А", 4))

@user.callback_query(F.data == 'Пятница9a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("9А", 5))


@user.message(F.text == '9Б')
async def cmd_hello(message: Message):
    await message.answer('''Ты выбрал класс - 9Б
Выбери расписание на день''',
                         reply_markup=kb.NineB)

@user.callback_query(F.data == 'Понедельник9b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("9Б", 1))

@user.callback_query(F.data == 'Вторник9b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("9Б", 2))

@user.callback_query(F.data == 'Среда9b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("9Б", 3))
    
@user.callback_query(F.data == 'Четверг9b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("9Б", 4))

@user.callback_query(F.data == 'Пятница9b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("9Б", 5))


@user.message(F.text == '9В')
async def cmd_hello(message: Message):
    await message.answer('''Ты выбрал класс - 9В
Выбери расписание на день''',
                         reply_markup=kb.NineV)

@user.callback_query(F.data == 'Понедельник9v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("9В", 1))

@user.callback_query(F.data == 'Вторник9v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("9В", 2))

@user.callback_query(F.data == 'Среда9v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("9В", 3))
    
@user.callback_query(F.data == 'Четверг9v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("9В", 4))

@user.callback_query(F.data == 'Пятница9v')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("9В", 5))



@user.message(F.text == '10А')
async def cmd_hello(message: Message):
    await message.answer('''Ты выбрал класс - 10А
Выбери расписание на день''',
                         reply_markup=kb.TenA)

@user.callback_query(F.data == 'Понедельник10a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("10А", 1))

@user.callback_query(F.data == 'Вторник10a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("10А", 2))

@user.callback_query(F.data == 'Среда10a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("10А", 3))
    
@user.callback_query(F.data == 'Четверг10a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("10А", 4))

@user.callback_query(F.data == 'Пятница10a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("10А", 5))


@user.message(F.text == '10Б')
async def cmd_hello(message: Message):
    await message.answer('''Ты выбрал класс - 10Б
Выбери расписание на день''',
                         reply_markup=kb.TenB)

@user.callback_query(F.data == 'Понедельник10b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("10Б", 1))

@user.callback_query(F.data == 'Вторник10b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("10Б", 2))

@user.callback_query(F.data == 'Среда10b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("10Б", 3))
    
@user.callback_query(F.data == 'Четверг10b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("10Б", 4))

@user.callback_query(F.data == 'Пятница10b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("10Б", 5))



@user.message(F.text == '11А')
async def cmd_hello(message: Message):
    await message.answer('''Ты выбрал класс - 11А
Выбери расписание на день''',
                         reply_markup=kb.ElevenA)

@user.callback_query(F.data == 'Понедельник11a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("11А", 1))

@user.callback_query(F.data == 'Вторник11a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("11А", 2))

@user.callback_query(F.data == 'Среда11a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("11А", 3))
    
@user.callback_query(F.data == 'Четверг11a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("11А", 4))

@user.callback_query(F.data == 'Пятница11a')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("11А", 5))


@user.message(F.text == '11Б')
async def cmd_hello(message: Message):
    await message.answer('''Ты выбрал класс - 11Б
Выбери расписание на день''',
                         reply_markup=kb.ElevenB)

@user.callback_query(F.data == 'Понедельник11b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("11Б", 1))

@user.callback_query(F.data == 'Вторник11b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("11Б", 2))

@user.callback_query(F.data == 'Среда11b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("11Б", 3))
    
@user.callback_query(F.data == 'Четверг11b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("11Б", 4))

@user.callback_query(F.data == 'Пятница11b')
async def check_class(callback: CallbackQuery):
    await callback.message.answer(schedule_1sm("11Б", 5))



@user.message()
async def echo(message: Message):
    await message.send_copy(chat_id=message.from_user.id)
    
