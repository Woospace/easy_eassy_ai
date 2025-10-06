# main.py (Cloud-Ready Version)

from flask import Flask, request, jsonify, send_from_directory, session, redirect, url_for
from flask_cors import CORS
from .llm_service import llm_service
import os

# --- 应用初始化 ---
# 将 app 的创建放在全局范围内，这是 WSGI 服务器 (如 Gunicorn) 发现和运行应用所必需的。
app = Flask(__name__)

# --- 安全配置 ---
# 1. CORS: 在生产环境中，应限制为仅允许您的前端域名访问，而不是 "*" (所有)。
#    例如: CORS(app, origins=["https://your-frontend-domain.onrender.com"])
CORS(app) 

# 2. 密钥管理: 所有敏感信息都必须从环境变量中读取，确保代码库中不包含任何机密。
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
CORRECT_ACCESS_CODE = os.environ.get('ACCESS_CODE')

# --- 安全响应头 ---
@app.after_request
def add_security_headers(response):
    """为所有响应添加安全头，禁用浏览器缓存，防止未授权用户通过浏览器历史返回访问受保护页面。"""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# --- 路由定义 ---

@app.route("/")
def serve_landing_page():
    # 使用相对安全的 send_from_directory 提供前端入口文件
    return send_from_directory("../FRONTEND", "landing.html")

@app.route("/index")
def serve_index_page():
    # 核心授权检查：确保在提供受保护内容前，session 中有有效的认证标志
    if session.get('authenticated'):
        return send_from_directory("../FRONTEND", "index.html")
    return redirect(url_for('serve_landing_page'))

@app.route("/verify_code", methods=["POST"])
def verify_access_code():
    data = request.get_json()
    if not data or "code" not in data:
        return jsonify({"success": False, "error": "无效请求"}), 400

    # 注意：为了防范暴力破解，生产环境应在此处增加速率限制 (rate limiting)
    if data["code"] == CORRECT_ACCESS_CODE:
        session['authenticated'] = True
        return jsonify({"success": True})
    else:
        session.pop('authenticated', None)
        return jsonify({"success": False, "error": "访问码不正确"}), 401

@app.route("/generate_outline", methods=["POST"])
def generate_outline_handler():
    if not session.get('authenticated'):
        return jsonify({"error": "未授权"}), 403

    data = request.get_json()
    # 确保关键数据存在，否则返回错误
    if not all(key in data for key in ["requirements", "rubric"]):
        return jsonify({"error": "请求缺少必要参数"}), 400

    subject = data.get("subject", "通用")
    try:
        outline = llm_service.generate_outline(subject, data["requirements"], data["rubric"])
        return jsonify({"outline": outline})
    except Exception as e:
        # 在服务器日志中记录详细错误，但返回给用户通用错误信息，避免泄露内部实现细节
        app.logger.error(f"Outline generation failed: {e}")
        return jsonify({"error": "服务器内部错误"}), 500

@app.route('/<path:filename>')
def serve_static_files(filename):
    # 统一处理所有其他前端静态文件请求
    return send_from_directory('../FRONTEND', filename)

# --- 移除本地开发服务器启动模块 ---
# 在生产环境中，永远不应该使用 app.run()。
# 应用的启动和运行完全由 Gunicorn 这样的 WSGI 服务器来管理。
# 移除此部分可以防止在配置错误时意外启动不安全的开发服务器。
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000, debug=True)