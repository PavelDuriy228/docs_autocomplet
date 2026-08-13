from yandex_form.model import FormLoader
from config import settings

form = FormLoader()
if settings.SURVEY_ID:
    form.load_data(settings.SURVEY_ID)
