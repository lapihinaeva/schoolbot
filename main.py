import sqlite3
import asyncio
import os
from dotenv import load_dotenv

from excel import second_grades, first_grades
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers import user
from excel import schedule_1sm, schedule_2sm
import asyncio
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter
from database import init_db, add_or_change, get_list_ids_by_grade  
from states import Registration, Registration_change       
from aiogram.filters import Command
from excel import update_sheet


async def broadcast_to_grade(bot: Bot, grade_key: str, func_shedule, day_num):
    update_sheet() 
    message_text = func_shedule(grade_key, day_num)
    
    user_ids = get_list_ids_by_grade(grade_key)
    for user_id in user_ids:
        try:
            current_id = user_id[0] if isinstance(user_id, tuple) else user_id
            await bot.send_message(chat_id=current_id, text=message_text)
            await asyncio.sleep(0.05) 
        except Exception as e:
            print(f"Ошибка отправки: {e}")


async def addJob(bot, grades, hours_workdays, minutes_workdays, scheduler, func_shedule):
    days_map = {
        'sun': 1,  # В Воскресенье на Понедельник
        'mon': 2,  # В Понедельник на Вторник
        'tue': 3,  
        'wed': 4,  
        'thu': 5   
    }

    for key in grades.keys():
        for day_code, day_num in days_map.items():
            
            h = 15 if day_code == 'sun' else hours_workdays
            m = 0 if day_code == 'sun' else minutes_workdays
            
            scheduler.add_job(
                broadcast_to_grade, 
                trigger='cron',
                day_of_week=day_code,
                hour=h, 
                minute=m, 
                args=[bot, key, func_shedule, day_num],
                id=f"sync_{key}_{day_code}", 
                replace_existing=True
            )


async def main():
    load_dotenv()
    init_db()
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_router(user)
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(update_sheet, "interval", minutes=2)

    await addJob(bot, first_grades, 12, 0, scheduler, schedule_1sm)
    await addJob(bot, second_grades, 16, 0, scheduler, schedule_2sm)
    
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


