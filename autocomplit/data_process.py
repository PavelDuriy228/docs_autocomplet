import pandas as pd


def process_form_data(input_file_path, output_file_path=None) -> list[dict]:
    # 1. Загружаем данные из формы (Excel или CSV)
    if input_file_path.endswith(".xlsx") or input_file_path.endswith(".xls"):
        df = pd.read_excel(input_file_path)
    else:
        df = pd.read_csv(input_file_path)

    # Очищаем названия колонок от лишних пробелов в начале/конце
    df.columns = df.columns.str.strip()

    # 2. Словарь соответствия: {"Название в форме": "Метка в шаблоне Word"}
    mapping = {
        "Фамилия": "surname",
        "Имя": "name",
        "Отчество": "patronymic",
        "Пол": "gender",
        "Дата рождения": "birth_date",
        "Институт": "institute",
        "Курс": "course",
        "Форма обучения": "study_form",
        "Серия и номер паспорта": "passport",
        "Семейное положение": "marital_status",
        "Номер телефона": "phone",
        "Страна постоянного проживания": "country",
        "Регион": "region",
        "Домашний адрес": "home_address",
        "Адрес Регистрации": "registration_address",
        "ФИО отца": "father_name",
        "Телефон отца": "father_phone",
        "ФИО матери": "mother_name",
        "Телефон матери": "mother_phone",
    }

    # 3. Переименовываем только те колонки, которые фактически присутствуют в таблице
    df = df.rename(columns=mapping)

    # 4. Формируем объединенное поле для домашнего адреса и телефона (если оба есть)
    # На карточке пункт 8 объединяет адрес и телефон
    if "home_address" in df.columns and "phone" in df.columns:
        df["home_address_phone"] = (
            df["home_address"].fillna("") + ", т. " + df["phone"].fillna("")
        )
    elif "home_address" in df.columns:
        df["home_address_phone"] = df["home_address"]

    df["das_num"] = "2"
    # 5. Список всех меток, используемых в документе Word
    doc_keys = [
        "das_num",
        "room_num",
        "group_num",
        "surname",
        "name",
        "patronymic",
        "birth_date",
        "gender",
        "check_in_date",
        "passport",
        "home_address_phone",
        "phone",
        "country",
        "marital_status",
        "father_name",
        "father_phone",
        "mother_name",
        "mother_phone",
    ]

    df["study_form"] = df["study_form"].replace(
        {
            "Бюджетное обучение": "г/б",
            "Внебюджетное обучение (платное)": "в/б",
            "Целевое обучение": "целевое",
        }
    )
    # 6. Добавляем отсутствующие метки с пустыми значениями
    for key in doc_keys:
        if key not in df.columns:
            df[key] = ""

    # 7. Преобразуем DataFrame в список словарей (по одной записи на студента)
    # Этот формат идеально подходить для заполнения шаблона Word через docxtpl
    students_records = df.to_dict(orient="records")

    # Опционально сохраняем обработанную таблицу
    if output_file_path:
        df.to_excel(output_file_path, index=False)

    return students_records


# --- Пример использования ---
if __name__ == "__main__":
    # Входные данные (список словарей из формы)
    students = process_form_data("data/2026-08-04 Заселение в ДАС-2 2026.csv")

    # Пример получившейся структуры для первой строки:
    print("Пример контекста для заполнения Word:")
    for row in pd.DataFrame(students).itertuples():
        print(row._2)
