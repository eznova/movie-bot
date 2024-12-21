#!/bin/bash -e

# Путь до проекта и директория для документации
PROJECT_DIR=$(pwd)
DOCS_DIR="$PROJECT_DIR/docs"

# Убедимся, что Sphinx установлен
if ! command -v sphinx-quickstart &> /dev/null
then
    echo "Sphinx не установлен. Установите его с помощью 'pip install sphinx'."
    pip3 install sphinx
fi

# Инициализация проекта Sphinx
echo "Инициализируем проект Sphinx..."
rm -rf $DOCS_DIR
sphinx-quickstart $DOCS_DIR --quiet --no-batchfile --project "My Python Project" --author "Your Name" --language "ru"

# Редактируем конфигурацию (conf.py)
echo "Редактируем конфигурацию Sphinx..."
CONF_DIR="$DOCS_DIR/source"
mkdir -p $CONF_DIR
CONF_FILE="$CONF_DIR/conf.py"


# Добавляем расширение autodoc
echo "extensions = ['sphinx.ext.autodoc']" >> $CONF_FILE

# Убедимся, что путь к Python добавлен в конфиг (для autodoc)
echo "Добавляем путь до исходных кодов..."
echo "import os" >> $CONF_FILE
echo "import sys" >> $CONF_FILE
echo "sys.path.insert(0, os.path.abspath('../src'))" >> $CONF_FILE

# Создаем файл index.rst
echo "Создаем файл index.rst..."
cat > $DOCS_DIR/source/index.rst <<EOL
.. My Python Project documentation master file, created by
   sphinx-quickstart on $(date).

Welcome to My Python Project's documentation!
===========================================

Contents:
=========
.. toctree::
   :maxdepth: 2
   :caption: Contents:

Modules
=======
.. automodule:: your_module_name
   :members:
   :undoc-members:
   :show-inheritance:
EOL

# Генерируем документацию
echo "Генерируем документацию..."
mkdir -p $DOCS_DIR/../../apidocs
sphinx-build -b html $DOCS_DIR/source $DOCS_DIR/../../apidocs
rm -rf $DOCS_DIR

# Сообщение об успехе
echo "Документация сгенерирована. Откройте файл $DOCS_DIR/_build/html/index.html для просмотра."
