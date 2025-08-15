#!/usr/bin/env python3
"""
本番環境用のWSGI起動スクリプト
gunicorn wsgi:app で起動
"""

import os
from app import app, db

if __name__ == "__main__":
    with app.app_context():
        # データベースの作成
        db.create_all()
        print("✅ データベースが作成されました")
    
    # 本番環境用の設定
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
