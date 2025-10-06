# config.py (v3 - Prompt as Env Var)

import os
from dotenv import load_dotenv

# 自动从项目根目录下的 .env 文件加载环境变量
load_dotenv()

# --- API 和 模型配置 ---
YOUR_LLM_API_KEY = os.getenv("YOUR_LLM_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_MODEL = "deepseek-chat"

# --- 新增：将 Prompt 也作为环境变量加载 ---
# 这样，llm_service.py 就不再需要读取文件了
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")

# --- 安全性检查 ---
if not YOUR_LLM_API_KEY:
    raise ValueError("错误：环境变量 'YOUR_LLM_API_KEY' 未设置。请检查 .env 文件。")
if not LLM_BASE_URL:
    raise ValueError("错误：环境变量 'LLM_BASE_URL' 未设置。请检查 .env 文件。")
if not SYSTEM_PROMPT:
    raise ValueError("错误：环境变量 'SYSTEM_PROMPT' 未设置。请将你的Prompt内容添加到 .env 文件中。")
