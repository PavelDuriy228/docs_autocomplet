from personal_card import PersonalCard
from autocomplit.data_process import process_form_data


def main():
    students = process_form_data("data/2026-08-04 Заселение в ДАС-2 2026.csv")
    personal_card = PersonalCard()
    personal_card.complit(students)


if __name__ == "__main__":
    main()
