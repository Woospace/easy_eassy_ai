# 智能写作大纲助手 (Intelligent Outline Generator)

这是一个基于大型语言模型（LLM）的 Web 应用，旨在帮助学生、研究人员和内容创作者快速生成结构化、逻辑严谨的学术论文或文章大纲。用户只需提供主题、具体要求和评分标准，即可获得一份高质量的写作框架，从而启发思路、提高写作效率。

## ✨ 已实现功能

* **安全访问控制**：通过访问码机制，确保服务不会被公开滥用。
* **简洁的 Web 界面**：提供清晰的前端界面，方便用户输入需求并清晰地展示生成的大纲。
* **高质量大纲生成**：后端集成兼容 OpenAI API 的大型语言模型，能够根据用户输入，产出深度、结构化的写作大纲。
* **配置与代码分离**：遵循生产环境最佳实践，所有敏感信息（如 API 密钥、应用密钥、核心 Prompt）均通过环境变量进行管理，代码库中不包含任何机密。

## 🛠️ 技术栈

* **后端**: Python, Flask, Gunicorn
* **前端**: HTML, CSS, JavaScript (Vanilla)
* **核心引擎**: 兼容 OpenAI API 的大语言模型 (例如 DeepSeek, Kimi, GPT-4 等)

## 🚀 本地运行指南

1.  **克隆仓库**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
    cd your-repo-name
    ```

2.  **创建并激活 Python 虚拟环境**
    ```bash
    python -m venv venv
    source venv/bin/activate  # on Windows, use `venv\Scripts\activate`
    ```

3.  **安装依赖**
    ```bash
    pip install -r requirements.txt
    ```

4.  **配置环境变量**
    * 复制环境变量模板文件：
        ```bash
        cp .env.example .env
        ```
    * 编辑 `.env` 文件，填入你自己的密钥和配置信息。

5.  **启动后端服务**
    ```bash
    python BACKEND/main.py
    ```
    服务将在 `http://127.0.0.1:8000` 启动。

## ☁️ 部署

本项目已为云平台部署做好准备（例如 Render, Heroku）。

* **Build Command**: `pip install -r requirements.txt`
* **Start Command**: `gunicorn main:app`

请确保在部署平台的“Environment”设置中配置好所有必要的环境变量。

## 📄 许可证

本项目采用 [MIT License](LICENSE) 授权。