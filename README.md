# Twitter transparent avatar setting tool

Flaskを運用して書かれた透過アバター設定ツール

# サーバー側にプログラムをデプロイする方法

## リポジトリの取得

```bash
git clone https://github.com/mitian233/twitter-transparent-avatar-setting-tool.git
cd twitter-transparent-avatar-setting-tool
```

## 依存パッケージをインストールする

```bash
pip3 install -r requirements.txt
```

## 環境設定

下記コマンドで、環境設定ファイルのサンプルをコピーします。

```bash
cp env.py.example env.py
```

それした後 `env.py` ファイル内の説明に従って編集してください。

## サーバーの起動

```bash
python3 app.py
# OR
gunicorn -b 127.0.0.1:<yourport> index:app
```

# Vercelでデプロイする方法

このプロジェクトが完成するまでお待ちください。