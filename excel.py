import openpyxl
import requests
import io
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


SHEET_ID = os.getenv("SHEET_ID")
EXPORT_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx'
book = None
sheet = None

def format_date(value):
    """Преобразует дату из ячейки в строку без времени"""
    if isinstance(value, datetime):
        return value.strftime('%d.%m.%Y')
    return str(value) if value is not None else ""

def update_sheet():
    """Скачивает свежую таблицу из Google в память бота"""
    global book, sheet
    try:
        response = requests.get(EXPORT_URL)
        if response.status_code == 200:
            book = openpyxl.load_workbook(filename=io.BytesIO(response.content), data_only=True)
            sheet = book.active
        else:
            print(f"Ошибка загрузки: статус {response.status_code}")
    except Exception as e:
        print(f"Критическая ошибка при обновлении таблицы: {e}")

update_sheet()

first_grades = {'5А':12,'5Б':13,'5В':14,'9А':15,'9Б':16,'9В':17,'10А':18,'10Б':19,'11А':20,'11Б':21}
second_grades = {'6А':2,'6Б':3,'6В':4,'7А':5,'7Б':6,'7В':7,'8А':8,'8Б':9,'8В':10}

ALLOWED_GRADES = list(first_grades.keys()) + list(second_grades.keys())

# вторая смена
def schedule_2sm(grade, week_day):
    if not (grade in second_grades) or not(week_day in [1,2,3,4,5]):
        return "Расписание не найдено"
    
    days_number = {1:2, 2:9, 3:16, 4:23, 5:30}
    start = days_number[week_day]
    column = second_grades[grade]
    end = start + 7
    
    date_header = format_date(sheet[start][0].value)
    resultString = date_header + '\n' if date_header else ""

    for row in range(start, end):
        time = str(sheet[row][1].value or '')
        raw_value = sheet[row][column].value
        clas = str(raw_value).strip() if raw_value else 'нет урока'
        resultString += time + '   ' + clas + "\n" 
    return resultString


# первая смена
def schedule_1sm(grade, week_day):
    if not (grade in first_grades) or not(week_day in [1,2,3,4,5]):
        return "Расписание не найдено"
    
    days_number = {1:2, 2:10, 3:18, 4:26, 5:34}
    start = days_number[week_day]
    column = first_grades[grade]
    end = start + 8
    
    date_header = format_date(sheet[start][0].value)
    resultString = date_header + '\n' if date_header else ""

    for row in range(start, end):
        time = str(sheet[row][11].value or '')
        raw_value = sheet[row][column].value
        clas = str(raw_value).strip() if raw_value else 'нет урока'
        resultString += time + '   ' + clas + "\n" 
    return resultString


