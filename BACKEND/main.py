# main.py (v6 - Anti-Cache Fix)

from flask import Flask, request, jsonify, send_from_directory, session, redirect, url_for
from flask_cors import CORS
from llm_service import llm_service
import os

app = Flask(__name__)
CORS(app)

# 注意：为了部署到Render，这些敏感值后续需要从环境变量读取
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
CORRECT_ACCESS_CODE = os.environ['ACCESS_CODE']

# --- 解决方案：添加 HTTP 头来禁用缓存 ---
@app.after_request
def add_header(response):
    """
    为所有响应添加 HTTP 头，指示浏览器不要缓存页面。
    这是为了确保每次访问受保护的页面时，都会执行服务器端的 session 检查，
    从而修复可以直接通过 URL 访问 /index 的缓存漏洞。
    """
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

print("--- 论文框架生成器API服务启动 ---")

@app.route("/")
def serve_landing_page():
    return send_from_directory("../FRONTEND", "landing.html")

@app.route("/index")
def serve_index_page():
    if 'authenticated' in session and session['authenticated']:
        return send_from_directory("../FRONTEND", "index.html")
    else:
        # 这里的重定向是服务器端强制执行的，是安全的核心
        return redirect(url_for('serve_landing_page'))

@app.route("/verify_code", methods=["POST"])
def verify_access_code():
    data = request.get_json()
    if not data or "code" not in data:
        return jsonify({"success": False, "error": "请求格式不正确"}), 400

    if data["code"] == CORRECT_ACCESS_CODE:
        session['authenticated'] = True
        return jsonify({"success": True})
    else:
        session.pop('authenticated', None)
        return jsonify({"success": False, "error": "访问码不正确"}), 401

@app.route("/generate_outline", methods=["POST"])
def generate_outline_handler():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({"error": "未授权的访问"}), 403

    data = request.get_json()
    subject = data.get("subject", "通用") # 增加默认值以提高容错性
    requirements = data["requirements"]
    rubric = data["rubric"]
    try:
        outline = llm_service.generate_outline(subject, requirements, rubric)
        return jsonify({"outline": outline})
    except Exception as e:
        print(f"[/generate_outline] 发生错误: {e}")
        return jsonify({"error": "服务器内部错误，生成失败"}), 500

@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory('../FRONTEND', filename)

if __name__ == "__main__":
    print("服务运行在 http://1227.0.0.1:8000")
    app.run(host="0.0.0.0", port=8000, debug=True)

