from yandex_form.model import FormLoader
from config import settings


def main():

    form = FormLoader()
    if settings.SURVEY_ID:
        form.load_data(settings.SURVEY_ID)


if __name__ == "__main__":
    main()
