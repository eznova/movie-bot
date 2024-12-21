#!/bin/bash -e

# Путь к директории, где находятся исходники документации
source .env
export YDB_DATABASE
export YDB_ENDPOINT
export KINOPOISK_API_KEY
export API_KEY
export FOLDER_ID

pushd $1

DOCS_DIR="./docs"
SOURCE_DIR="$DOCS_DIR/source"
BUILD_DIR="$DOCS_DIR/_build"

# Проверяем, существует ли директория для документации
if [ ! -d "$DOCS_DIR" ]; then
  echo "Создаю директорию для документации: $DOCS_DIR"
  mkdir -p "$DOCS_DIR" "$SOURCE_DIR"
fi

project_dir=$(pwd)

# Создаём конфигурационный файл conf.py для Sphinx
cat > "$SOURCE_DIR/conf.py" <<EOL
import os
import sys
sys.path.insert(0, os.path.abspath('${project_dir}'))  # Добавляем корневую директорию в sys.path

# -- Основная информация о проекте ---------------------------------------

project = 'Movie Search Bot'  # Название проекта
author = 'Offline Command'  # Имя автора
release = '1.0'  # Версия

# -- Расширения ------------------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',  # Для автоматической документации
    'sphinx.ext.viewcode',  # Для отображения исходного кода
]

# -- Параметры документации -----------------------------------------------

templates_path = ['_templates']
exclude_patterns = []

# -- HTML выход -----------------------------------------------------------

html_theme = 'alabaster'  # Тема документации
html_static_path = ['_static']
EOL

echo "Конфигурационный файл conf.py успешно создан."

# Создаём основной файл index.rst
cat > "$SOURCE_DIR/index.rst" <<EOL
.. Movie Search Bot documentation master file, created by
   sphinx-quickstart on <дата>.

Welcome to Movie Search Bot's documentation!
===========================================

Contents:
=========
.. toctree::
   :maxdepth: 2
   :caption: Contents:

Modules
=======
.. automodule:: index
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: films
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: kinopoisk_api
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: process_database
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: process_opinion
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: sessions
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: yandexgpt_api
   :members:
   :undoc-members:
   :show-inheritance:
EOL

echo "Файл index.rst успешно создан."

# Убедимся, что у нас установлен Sphinx, и если не установлен, то устанавливаем его
if ! command -v sphinx-build &> /dev/null; then
    echo "Sphinx не найден. Устанавливаю Sphinx..."
    pip install sphinx
fi

# Генерация документации
echo "Генерируем документацию..."

# Путь для выходной документации
OUTPUT_DIR="../docs/apidocs"

# Удаляем старую документацию, если существует, и создаём новую папку
rm -rf "$OUTPUT_DIR" && mkdir -p "$OUTPUT_DIR"

# Запуск Sphinx для генерации документации
sphinx-build -b html "$SOURCE_DIR" "$OUTPUT_DIR"

# Сообщение об успехе
echo "Документация сгенерирована. Откройте файл $OUTPUT_DIR/index.html для просмотра."

# Убираем временные файлы документации
rm -rf "$DOCS_DIR"

popd