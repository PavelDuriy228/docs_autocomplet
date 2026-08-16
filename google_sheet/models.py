from google_sheet.sheet_integration import SheetDriver
from pandas import DataFrame
from config import settings


class ToSheetFormater:

    def __init__(self, spreadsheetId: str | None = settings.SPREADSHEET_ID) -> None:
        self.driver = SheetDriver(spreadsheetId)

    def add(self, students_records):
        students_records = DataFrame(students_records)
        # Добавляем только уникальные паспорты
        pasport_in_sheet = [
            str(pasport[0]) for pasport in self.driver.get(range="H2:H")
        ]

        to_save = students_records[~students_records["passport"].isin(pasport_in_sheet)]

        formatted = self._format(to_save)
        self.driver.append(formatted)

    # Google Sheet Table
    # ID	ФИО	Статус	Номер комнаты	Институт	№ Группы	Курс	г/б в/б	Паспорт	Регион	Дата рождения	Номер телефона	Дата заселения	Справка 086у/сифилис	Флюра до	Оплата	Паспорт	сергеев	Акты			прописка	журнал

    # Local Table
    # ['ID', 'surname', 'name', 'patronymic', 'gender',
    #        'birth_date', 'institute', 'course', 'study_form', 'passport',
    #        'marital_status', 'phone', 'country', 'region', 'home_address',
    #        'registration_address', 'father_name', 'father_phone', 'mother_name',
    #        'mother_phone', 'home_address_phone', 'das_num', 'room_num',
    #        'group_num', 'check_in_date']

    def _format(self, df: DataFrame) -> list[list]:
        """Здесь приводим в порядок строки из локальной таблицы к формату таблицы на google sheet"""
        to_save = []
        df["phone"] = df["phone"].str.replace("+", "'+", regex=False)
        for row in df.itertuples():
            to_save.append(
                [
                    row.ID,
                    f"{row.surname} {row.name} {row.patronymic}",
                    "NEW",
                    "",
                    row.institute,
                    row.group_num,
                    row.course,
                    row.study_form,
                    row.passport,
                    (
                        row.region
                        if row.country != "Россия" and row.country != "Russia"
                        else row.country
                    ),
                    row.birth_date,
                    row.phone,
                ]
            )
        return to_save
