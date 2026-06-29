# Zapret Installer

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Witlg/zapret-installer)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Windows](https://img.shields.io/badge/platform-Windows-0078d7.svg)](https://www.microsoft.com/windows)

Простой установщик для Zapret - инструмента обхода DPI для Discord, YouTube и игр.

##  Скачать

**[Скачать установщик](https://github.com/yourusername/zapret-installer/releases/latest/download/setup.exe)**

## Особенности

- Один файл установщика
-  Все файлы уже внутри
-  Красивый графический интерфейс
-  Выбор пути установки
-  Создание ярлыков на рабочем столе и в меню Пуск
-  Автоматический запрос прав администратора

##  Быстрый старт

1. Скачайте `setup.exe`
2. Запустите файл
3. Выберите папку для установки
4. Нажмите "Install"

##  Для разработчиков

### Сборка из исходников

```bash
# Клонировать репозиторий
git clone https://github.com/Witlg/zapret-installer.git
cd zapret-installer

# Установить зависимости
pip install pyinstaller PyQt6

# Собрать установщик
python build_setup.py
