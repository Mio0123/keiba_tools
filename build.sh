#!/bin/bash

# 依存関係をインストール
pip install --upgrade pip
pip install -r requirements.txt

# Djangoのビルドコマンドを実行
python3 manage.py collectstatic --noinput
python3 manage.py migrate