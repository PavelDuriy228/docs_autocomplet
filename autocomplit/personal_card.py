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
            doc = DocxTemplate(self.doc_path)

            doc.render(context=student_context)

            surname = str(student_context.get("surname", "Неизвестно")).strip()
            name = str(student_context.get("name", "Неизвестно")).strip()
            birth_date = str(student_context.get("birth_date", "Неизвестно")).strip()

            if (
                surname == "Неизвестно"
                or name == "Неизвестно"
                or birth_date == "Неизвестно"
            ):
                print(f"[WARN] Есть неизвестные поля {student_context}")

            student_path = (
                f"{surname}_{name}_{student_context['birth_date']}_{birth_date}"
            )
            self._save_doc(student_path, doc)

    def _save_doc(self, student: str, doc: DocxTemplate):
        student = re.sub(r'[\\/*?:"<>.|]', "", student)
        path = (
            self.output_path + student
        )  # путь до папок студенто + папка самого студента
        # У каждого студента должна быть своя папка
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)

        doc.save(f"{path}/Личная_Карточка_{student}.docx")
        print(f"Карточка студента {student} сохранена в {path} ")
