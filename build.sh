#!/bin/bash

# 依存関係をインストール
pip install -r requirements.txt

# CSSなどを収集
python3 manage.py collectstatic --noinput

# データベースのマイグレーションを実行
python3 manage.py migrate