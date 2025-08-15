import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """基本設定クラス"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OpenAI設定
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # データベース設定
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///chat_history.db')
    
    # セキュリティ設定
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    PORT = int(os.getenv('PORT', 5000))
    
    # ログ設定
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

class DevelopmentConfig(Config):
    """開発環境用設定"""
    FLASK_DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///chat_history.db'

class ProductionConfig(Config):
    """本番環境用設定"""
    FLASK_DEBUG = False
    # PostgreSQLを使用する場合
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class TestingConfig(Config):
    """テスト環境用設定"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# 設定の選択
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
