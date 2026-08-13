import requests
from config import settings
from datetime import datetime
import sys
import time


class FormLoader:
    HEADERS = {
        "Authorization": f"OAuth {settings.FORMS_TOKEN}",
        "X-Cloud-Org-Id": settings.ORG_ID,
    }

    def start_export(self, survey_id: str, format: str) -> str | None:
        """
        Запускает фоновый процесс экспорта ответов.
        Возвращает код запущенной операции.
        """
        url = f"{settings.FORMS_PUBLIC_API}/surveys/{survey_id}/answers/export"
        params = {"format": format}
        response = requests.post(url, json=params, headers=self.HEADERS)
        if response.status_code == 202:
            result = response.json()
            operation_id = result.get("id")
            return operation_id
        print(response.status_code, response.json())
        return None

    def check_finished(self, operation_id: str) -> bool:
        url = f"{settings.FORMS_PUBLIC_API}/operations/{operation_id}"
        response = requests.get(url, headers=self.HEADERS)
        if response.status_code == 200:
            result = response.json()
            return result.get("status") == "ok"
        return False

    def download_result(self, survey_id: str, operation_id: str) -> bytes | None:
        url = f"{settings.FORMS_PUBLIC_API}/surveys/{survey_id}/answers/export-results"
        params = {"task_id": operation_id}
        response = requests.get(url, params=params, headers=self.HEADERS)
        if response.status_code == 200:
            return response.content
        return None

    def write_data(self, content, output_path: str):
        with open(output_path, "wb") as f:
            f.write(content)

        print(f"Ответы выгружены в файл {output_path}")

    def load_data(
        self, survey_id: str, output_path: str | None = None, format: str = "csv"
    ):
        operation_id = self.start_export(survey_id, format)
        if operation_id:
            print(f"Запущена операция {operation_id}")

            i = 0
            while not self.check_finished(operation_id) and i < 30:
                print("...")
                time.sleep(5)
            if i == 30:
                print("[WARN] Превышен лимит ожидания файла")

            content = self.download_result(survey_id, operation_id)
            if content:
                if not output_path:
                    output_path = f"data/{survey_id}.{format}"
                self.write_data(content, output_path)
            else:
                print("[ERROR] Не удалось получить данные")
