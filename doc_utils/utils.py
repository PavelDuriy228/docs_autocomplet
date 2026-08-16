import os
import shutil


def get_archive(
    path: str, output_path: str, rewrite: bool = False, format: str = "zip"
) -> bool:
    print(os.getcwd())
    if not os.path.exists(path):
        print(f"[INFO] Указанного пути {path} не существует!")
        return False

    # Путь к архиву без расширения (создастся файл my_archive.zip) и путь к папке
    if os.path.exists(output_path):
        if rewrite:
            shutil.make_archive(output_path, format, path)
            print("[INFO] Архив уже существует и произошла перезапись")
            return True
        return False

    shutil.make_archive(output_path, format, path)
    print(f"[INFO] Создан архив в {output_path}")
    return True
