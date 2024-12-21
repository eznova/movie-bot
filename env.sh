#!/bin/bash
source .env
export YDB_DATABASE
export YDB_ENDPOINT
export KINOPOISK_API_KEY
export API_KEY
export FOLDER_ID

pushd $1 && python3 app.py
popd