import subprocess
import sys

# Список необходимых библиотек
required_packages = ['cryptography', 'pygame', 'datetime']

def install_packages(packages):
    print("Проверка и установка необходимых библиотек...")
    for package in packages:
        try:
            __import__(package)
            print(f"Библиотека {package} уже установлена.")
        except ImportError:
            print(f"Библиотека {package} не найдена. Установка...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Библиотека {package} успешно установлена.")

install_packages(required_packages)
print("\n\n\n")
input("Установка завершена, нажмите клавишу enter...")