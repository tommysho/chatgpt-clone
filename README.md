# ChatGPT Clone - 本番環境デプロイガイド

## 🚀 概要

このプロジェクトは、OpenAI APIを使用したChatGPTライクなWebサービスです。
Flask + SQLAlchemy + OpenAI APIで構築されており、会話履歴の保存と文脈保持機能を備えています。

## 📋 機能

- ✅ ChatGPTライクなチャット機能
- ✅ 会話履歴の永続化（SQLite/PostgreSQL）
- ✅ セッション管理
- ✅ 文脈保持（過去の会話を参照）
- ✅ レスポンシブなWeb UI

## 🛠️ 技術スタック

- **Backend**: Flask + SQLAlchemy
- **Database**: SQLite（開発） / PostgreSQL（本番）
- **AI**: OpenAI GPT-4o-mini
- **Frontend**: HTML + CSS + JavaScript
- **Deployment**: Gunicorn + WSGI

## 🚀 本番環境へのデプロイ

### 1. Render へのデプロイ（推奨）

#### 手順

1. **GitHubにプロジェクトをプッシュ**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Renderで新しいWeb Serviceを作成**
   - [Render Dashboard](https://dashboard.render.com/) にアクセス
   - "New +" → "Web Service" を選択
   - GitHubリポジトリを接続

3. **設定**
   - **Name**: `chatgpt-clone`（任意）
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app`

4. **環境変数を設定**
   ```
   FLASK_ENV=production
   FLASK_DEBUG=False
   SECRET_KEY=your-super-secret-key-here
   OPENAI_API_KEY=sk-your-openai-api-key
   DATABASE_URL=postgresql://...（RenderのPostgreSQLアドオンから取得）
   ```

5. **デプロイ**
   - "Create Web Service" をクリック
   - ビルド完了まで待機

### 2. Railway へのデプロイ

#### 手順

1. **Railwayにプロジェクトを接続**
   - [Railway](https://railway.app/) にアクセス
   - GitHubリポジトリを接続

2. **環境変数を設定**
   - プロジェクト設定で環境変数を追加
   - 上記と同じ環境変数を設定

3. **デプロイ**
   - 自動でデプロイが開始される

## 🔧 本番環境用の設定

### 環境変数

```bash
# 必須
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-super-secret-key-here
OPENAI_API_KEY=sk-your-openai-api-key

# データベース（PostgreSQL推奨）
DATABASE_URL=postgresql://username:password@host:port/database_name

# オプション
PORT=5000
LOG_LEVEL=INFO
```

### データベース移行（SQLite → PostgreSQL）

1. **PostgreSQLアドオンを追加**
   - Render/RailwayでPostgreSQLアドオンを有効化

2. **環境変数を更新**
   - `DATABASE_URL`をPostgreSQLの接続文字列に変更

3. **データベースを再作成**
   - アプリが自動的に新しいデータベースを作成

## 📁 ファイル構成

```
chatgpt-clone/
├── app.py              # メインアプリケーション
├── models.py           # データベースモデル
├── config.py           # 設定管理
├── wsgi.py             # 本番環境用起動スクリプト
├── requirements.txt    # 依存関係
├── templates/          # HTMLテンプレート
│   └── index.html     # メインページ
└── README.md           # このファイル
```

## 🔒 セキュリティ

- デバッグモードは本番環境で無効化
- 環境変数で機密情報を管理
- CORS設定で許可されたドメインのみアクセス許可
- レート制限でAPIの過度な使用を防止

## 📊 パフォーマンス

- Gunicornでマルチワーカー起動
- データベース接続プール
- 静的ファイルのキャッシュ

## 🚨 トラブルシューティング

### よくある問題

1. **データベース接続エラー**
   - `DATABASE_URL`の形式を確認
   - PostgreSQLアドオンが有効化されているか確認

2. **OpenAI APIエラー**
   - `OPENAI_API_KEY`が正しく設定されているか確認
   - APIキーの有効期限と使用制限を確認

3. **ビルドエラー**
   - Python 3.8以上を使用
   - `requirements.txt`の依存関係を確認

## 📞 サポート

問題が発生した場合は、以下を確認してください：

1. Render/Railwayのログ
2. 環境変数の設定
3. データベース接続
4. OpenAI APIキーの有効性

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。
