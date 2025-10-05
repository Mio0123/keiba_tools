# ベースとなるPythonの公式イメージを指定
FROM python:3.10-slim

# 環境変数を設定（Pythonのバッファリングを無効化）
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 作業ディレクトリを作成・設定
WORKDIR /app

# 必要なライブラリをインストール
COPY requirements.txt /app/

# ▼▼▼【重要】ここが修正・追加した部分です ▼▼▼
# pipのアップグレードと、mysqlclientのビルドに必要なOSパッケージをインストール
RUN pip install --upgrade pip && \
    apt-get update && \
    apt-get install -y build-essential pkg-config default-libmysqlclient-dev

# requirements.txt に基づいてPythonライブラリをインストール
RUN pip install -r requirements.txt

# プロジェクトファイルをコンテナにコピー
COPY . /app/

# コンテナ起動時に実行するコマンド
# ここではひとまず何もしない（docker-composeで上書きするため）
CMD ["echo", "Container is ready"]