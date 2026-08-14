from yandex_form.model import FormLoader
from autocomplit.data_process import process_form_data
from google_sheet.models import ToSheetFormater
from config import settings


def main():
    google_formater = ToSheetFormater()
    # Входные данные (список словарей из формы)
    students = process_form_data("data/2026-08-04 Заселение в ДАС-2 2026.csv")
    google_formater.add(students)


if __name__ == "__main__":
    main()
