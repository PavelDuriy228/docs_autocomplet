import os

path2_docs = "data/students_data"


def get_student_dirs() -> list[str]:
    folders = [f.name for f in os.scandir(path2_docs) if f.is_dir()]
    return folders
