from yandex_form.model import FormLoader
from doc_utils.personal_card import PersonalCard
from doc_utils.data_process import process_form_data
from google_sheet.models import ToSheetFormater
from config import settings


async def run_pipline() -> bool:
    try:
        form = FormLoader()
        google_formater = ToSheetFormater()
        personal_card = PersonalCard()

        if settings.SURVEY_ID:
            # загружаем данные
            form.load_data(settings.SURVEY_ID, output_path="data/yandex_form.csv")

        # Приводим в порядок таблицу с студентами
        students = process_form_data("data/yandex_form.csv")
        # Заполняем документ
        personal_card.complit(students)
        # загружаем на гугл таблицу
        google_formater.add(students)
        return True
    except:
        return False
