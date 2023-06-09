
import lib.copydetect
from lib.copydetect import CopyDetector
import pygments
import shutil
import os

excluded_dirs = ['Properties','obj']

dir_path = os.path.dirname(os.path.realpath(__file__))+"/data"

base_files_dir = input("Папка с файлами по умолчанию (можно не указывать): ")
if base_files_dir != "":
    base_files_dir = dir_path + "/" + base_files_dir
task_dir = input("Введите название папки с заданиями: ")

counter = 1
test_dirs = []

for student in os.listdir(path=dir_path):
    cur_student_task_dir = task_dir
    files = os.listdir(path=dir_path+"/"+student)
    if task_dir not in files:
        dirs = {}
        print(student + ": папка не обнаружена")
        print("Доступные варианты: ")
        counter = 0
        for stud_dir in files:
            if os.path.isdir(dir_path+"/"+student+"/"+stud_dir):
                print(str(counter)+")", stud_dir)
                dirs[counter] =  stud_dir
                counter += 1
        print(str(counter)+")", "Нужной папки нет")
        task_dir_num = int(input())
        if (task_dir_num == counter):
            print("Репозиторий студента", student, "исключён из проверки")
            continue
        else:
            cur_student_task_dir = dirs[task_dir_num]
            print("Для студента", student, "выбрана папка", cur_student_task_dir)

    else:
        print(student+": папка обнаружена")
    detected_dir = dir_path+"/"+student+"/"+cur_student_task_dir
    test_dirs.append(detected_dir)
    for stud_root, stud_dirs, stud_files in os.walk(detected_dir):
        for stud_dir in stud_dirs:
            if stud_dir in \
                    excluded_dirs:
                shutil.rmtree(stud_root+'/'+stud_dir)


print(test_dirs)
if base_files_dir == "":
    detector = CopyDetector(test_dirs=test_dirs, extensions=["cs"], display_t=0.5)
else:
    detector = CopyDetector(test_dirs=test_dirs, boilerplate_dirs=base_files_dir, extensions=["cs"], display_t=0.5)
detector.add_file("copydetect/utils.py")
detector.run()

detector.generate_html_report()