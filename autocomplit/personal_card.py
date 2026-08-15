import re
import os
from typing import Any, Dict, cast
from pandas import DataFrame
from docxtpl import DocxTemplate


class PersonalCard:
    # Загружаем сохраненный шаблон карточки
    doc_path = "docs_template/student_card_template.docx"
    output_path = "data/students_data/"

    def __init__(
        self, output_path: str | None = None, doc_path: str | None = None
    ) -> None:
        if doc_path:
            self.doc_path = doc_path
        if output_path:
            self.output_path = output_path

    def complit(self, df: list[dict]):

        for student_context in df:
            surname = str(student_context.get("surname", "Неизвестно")).strip()
            name = str(student_context.get("name", "Неизвестно")).strip()
            birth_date = str(student_context.get("birth_date", "Неизвестно")).strip()

            student = f"{surname}_{name}_{birth_date}"
            student = re.sub(r'[\\/*?:"<>.|]', "", student)

            if self._exist_file(student):
                continue

            doc = DocxTemplate(self.doc_path)

            doc.render(context=student_context)

            if (
                surname == "Неизвестно"
                or name == "Неизвестно"
                or birth_date == "Неизвестно"
            ):
                print(f"[WARN] Есть неизвестные поля {student_context}")

            self._save_doc(student, doc)

    def _exist_file(self, student: str):
        file_name = f"Личная_Карточка_{student}.docx"
        if os.path.exists(self.output_path + student + "/" + file_name):
            print(f"[INFO] {file_name} уже существует")
            return True
        return False

    def _save_doc(self, student: str, doc: DocxTemplate):

        path = (
            self.output_path + student
        )  # путь до папок студенто + папка самого студента
        # У каждого студента должна быть своя папка
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)

        doc.save(f"{path}/{student}.docx")
        print(f"Карточка студента {student} сохранена в {path} ")
