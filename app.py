from flask import Flask, request, jsonify, render_template, session
from openai import OpenAI
import os
from dotenv import load_dotenv
import traceback
import uuid
from models import db, ChatSession, ChatMessage

load_dotenv()



# OpenAI APIキーの確認
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("⚠️ 警告: OPENAI_API_KEYが設定されていません")
    print("📝 .envファイルを作成して、OPENAI_API_KEYを設定してください")
    print("例: OPENAI_API_KEY=sk-your-api-key-here")
    client = None
else:
    print("✅ OpenAI APIキーが設定されています")
    print(f"🔑 APIキー: {api_key[:20]}...")
    # OpenAIクライアントの初期化
    client = OpenAI(api_key=api_key)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')  # セッション管理用
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///chat_history.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# データベースの初期化
db.init_app(app)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({"status": "ok"})

@app.route("/chat", methods=["POST"])
def chat():
    print("🔍 チャットAPIが呼び出されました")
    
    if not api_key or not client:
        print("❌ APIキーが設定されていません")
        return jsonify({"error": "OpenAI APIキーが設定されていません"}), 500
    
    try:
        # リクエストデータの確認
        print(f"📥 リクエストヘッダー: {dict(request.headers)}")
        print(f"📥 リクエストボディ: {request.get_data()}")
        
        data = request.get_json(silent=True) or {}
        print(f"📥 パースされたJSON: {data}")
        
        user_message = (data.get("message") or "").strip()
        if not user_message:
            print("❌ メッセージが含まれていません")
            return jsonify({"error": "メッセージが含まれていません"}), 400
        
        print(f"💬 ユーザーメッセージ: {user_message}")
        
        # セッションIDの取得または作成
        session_id = data.get("session_id")
        if not session_id:
            session_id = str(uuid.uuid4())
            print(f"🆔 新しいセッションIDを作成: {session_id}")
        
        # セッションの取得または作成
        chat_session = ChatSession.query.filter_by(session_id=session_id).first()
        if not chat_session:
            chat_session = ChatSession(session_id=session_id)
            db.session.add(chat_session)
            print(f"📝 新しいチャットセッションを作成: {session_id}")
        
        # ユーザーメッセージをデータベースに保存
        user_msg = ChatMessage(
            session_id=session_id,
            role='user',
            content=user_message
        )
        db.session.add(user_msg)
        
        # 過去の会話履歴を取得（文脈保持のため）
        previous_messages = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.timestamp).all()
        
        # OpenAI API用のメッセージ履歴を作成
        messages_for_api = []
        for msg in previous_messages:
            messages_for_api.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # 最新のユーザーメッセージを追加
        messages_for_api.append({
            "role": "user",
            "content": user_message
        })
        
        print(f"📚 会話履歴: {len(messages_for_api)}件のメッセージ")
        
        # OpenAI API呼び出し（最新の記法）
        print("🚀 OpenAI APIを呼び出しています...")
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # 現行で軽くて安いモデル
            messages=messages_for_api,
            temperature=0.7,
        )
        
        print(f"✅ OpenAI APIレスポンス: {completion}")
        
        ai_reply = completion.choices[0].message.content
        print(f"💬 AI応答: {ai_reply}")
        
        # AIの応答をデータベースに保存
        ai_msg = ChatMessage(
            session_id=session_id,
            role='assistant',
            content=ai_reply
        )
        db.session.add(ai_msg)
        
        # データベースに保存
        db.session.commit()
        print(f"💾 データベースに保存完了: セッション {session_id}")
        
        return jsonify({
            "response": ai_reply,
            "session_id": session_id
        })
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {str(e)}")
        print(f"❌ エラータイプ: {type(e).__name__}")
        print(f"❌ スタックトレース: {traceback.format_exc()}")
        return jsonify({"error": f"API呼び出しエラー: {str(e)}"}), 500

@app.route("/api/history/<session_id>", methods=["GET"])
def get_chat_history(session_id):
    """特定のセッションの会話履歴を取得"""
    try:
        chat_session = ChatSession.query.filter_by(session_id=session_id).first()
        if not chat_session:
            return jsonify({"error": "セッションが見つかりません"}), 404
        
        messages = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.timestamp).all()
        
        history = []
        for msg in messages:
            history.append({
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat()
            })
        
        return jsonify({
            "session_id": session_id,
            "history": history
        })
        
    except Exception as e:
        print(f"❌ 履歴取得エラー: {str(e)}")
        return jsonify({"error": f"履歴取得エラー: {str(e)}"}), 500

@app.route("/api/sessions", methods=["GET"])
def get_sessions():
    """全セッション一覧を取得"""
    try:
        sessions = ChatSession.query.order_by(ChatSession.updated_at.desc()).all()
        
        session_list = []
        for session in sessions:
            session_list.append({
                "session_id": session.session_id,
                "created_at": session.created_at.isoformat(),
                "updated_at": session.updated_at.isoformat(),
                "message_count": len(session.messages)
            })
        
        return jsonify({"sessions": session_list})
        
    except Exception as e:
        print(f"❌ セッション一覧取得エラー: {str(e)}")
        return jsonify({"error": f"セッション一覧取得エラー: {str(e)}"}), 500

if __name__ == "__main__":
    with app.app_context():
        # データベースの作成
        db.create_all()
        print("✅ データベースが作成されました")
    
    # 本番環境用の設定
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    
    app.run(
        host='0.0.0.0',  # 外部アクセスを許可
        port=port,
        debug=debug_mode,  # 環境変数で制御
        use_reloader=False  # デバッガの多重起動を防止
    )
