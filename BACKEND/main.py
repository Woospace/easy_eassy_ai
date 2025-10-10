# main.py

import os
import firebase_admin
from functools import wraps
from firebase_admin import credentials, auth
from flask import Flask, request, jsonify, send_from_directory, session, redirect, url_for
from flask_cors import CORS
from .llm_service import llm_service

# --- App Initialization ---
app = Flask(__name__)
CORS(app)
# SECRET_KEY 建议从环境变量加载，以确保生产环境安全
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a-very-secret-key-for-dev')

# --- Firebase Admin SDK Initialization ---
# 自动适配 Render 部署环境与本地开发环境的凭证路径
try:
    render_secret_path = "/etc/secrets/firebase_credentials_json"
    local_relative_path = os.path.join(os.path.dirname(__file__), '..', 'easy-essay-ai-firebase-adminsdk-fbsvc-866e0e5dc6.json')

    if os.path.exists(render_secret_path):
        cred_path = render_secret_path
    elif os.path.exists(local_relative_path):
        cred_path = local_relative_path
    else:
        raise FileNotFoundError("Firebase credentials JSON not found.")

    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    app.logger.info("Firebase Admin SDK initialized successfully.")
except Exception as e:
    app.logger.critical(f"FATAL: Failed to initialize Firebase Admin SDK: {e}")

# --- Decorator for Authentication ---
def login_required(f):
    """
    一个装饰器，用于保护需要用户登录才能访问的路由。
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            # API请求返回JSON错误，页面请求重定向到登录页
            if request.path.startswith('/generate_outline'):
                 return jsonify({"error": "Unauthorized"}), 403
            return redirect(url_for('serve_landing_page'))
        return f(*args, **kwargs)
    return decorated_function

# --- Security Headers ---
@app.after_request
def add_security_headers(response):
    """为所有响应添加安全头，禁用浏览器缓存。"""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# --- Route Definitions ---

@app.route("/")
def serve_landing_page():
    """提供公共的登录页面。"""
    return send_from_directory("../FRONTEND", "landing.html")

@app.route("/index")
@login_required
def serve_index_page():
    """提供受保护的主应用页面。"""
    return send_from_directory("../FRONTEND", "index.html")

@app.route("/google-login", methods=["POST"])
def google_login():
    """验证前端发送的Google ID Token，并创建用户会话。"""
    token = request.json.get("token")
    if not token:
        return jsonify({"success": False, "error": "ID Token is missing"}), 400

    try:
        decoded_token = auth.verify_id_token(token)
        session['authenticated'] = True
        session['uid'] = decoded_token['uid']
        return jsonify({"success": True})
    except Exception as e:
        app.logger.error(f"Token verification failed: {e}")
        return jsonify({"success": False, "error": "Invalid or expired ID Token"}), 401

@app.route("/generate_outline", methods=["POST"])
@login_required
def generate_outline_handler():
    """处理生成大纲的API请求，调用LLM服务。"""
    data = request.get_json()
    if not all(key in data for key in ["requirements", "rubric"]):
        return jsonify({"error": "Missing required parameters"}), 400

    subject = data.get("subject", "通用")
    try:
        outline = llm_service.generate_outline(subject, data["requirements"], data["rubric"])
        return jsonify({"outline": outline})
    except Exception as e:
        app.logger.error(f"Outline generation failed: {e}")
        return jsonify({"error": "Internal server error during outline generation"}), 500

@app.route('/<path:filename>')
def serve_static_files(filename):
    """统一处理所有前端静态文件的请求（如CSS, JS文件）。"""
    return send_from_directory('../FRONTEND', filename)