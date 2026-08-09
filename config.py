import os
from dotenv import load_dotenv
import json

load_dotenv()


class Settings:
    FORMS_PUBLIC_API = os.getenv("FORMS_PUBLIC_API")
    FORMS_TOKEN = os.getenv("OATH_TOKEN")
    ORG_ID = os.getenv("ORG_ID")
    SURVEY_ID = os.getenv("SURVEY_ID")


# class MetaData:
#     file_name = "metadata.json"
#     data = {"last_download": 0.0}
#     _data_read = False

#     def __init__(self):
#         if not os.path.exists(self.file_name):
#             self.write_file()
#         if not self._data_read:
#             self.read()

#     def write_file(self):
#         with open(self.file_name, "w", encoding="utf-8") as f:
#             json.dump(self.data, f, ensure_ascii=False, indent=4)
#         print("[INFO] Создан/Перезаписан файл с метадатой")

#     def read(self):
#         with open(self.file_name, "r", encoding="utf-8") as f:
#             self.data = json.load(f)
#         self._data_read = True

#     def get(self, key: str):
#         return self.data.get(key, None)

#     def add(self, key: str, value):
#         self.data[key] = value

#     def write(self, key: str, value):
#         self.data[key] = value
#         if not os.path.exists(self.file_name):
#             self.write_file()


settings = Settings()
# meta = MetaData()
