// FilePath: FRONTEND/main.js

// --- 接口定义 ---
// const API_URL = 'http://127.0.0.1:8000/generate_outline';
const API_URL = '/generate_outline';
const outlineForm = document.getElementById('outline-form');
const generateBtn = document.getElementById('generate-btn');
const statusDisplay = document.getElementById('status-display');
const resultContainer = document.getElementById('result-container');
const outputPanel = document.querySelector('.output-panel'); // [新增] 获取输出面板元素

// --- 核心联动逻辑 ---
outlineForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    generateBtn.disabled = true;
    statusDisplay.classList.remove('status-hidden');
    resultContainer.innerHTML = '';
    outputPanel.classList.add('is-thinking'); // [新增] 开始动画

    const subject = document.getElementById('subject').value;
    const requirements = document.getElementById('requirements').value;
    const rubric = document.getElementById('rubric').value;

    if (!subject.trim() || !requirements.trim()) {
        resultContainer.innerHTML = '<p class="result-error">错误：学科主题和作业要求不能为空！</p>';
        generateBtn.disabled = false;
        statusDisplay.classList.add('status-hidden');
        outputPanel.classList.remove('is-thinking'); // [新增] 错误时也要停止动画
        return;
    }

    const requestData = {
        subject: subject,
        requirements: requirements,
        rubric: rubric
    };

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `服务器错误，状态码: ${response.status}`);
        }

        const data = await response.json();

        // 使用 marked.js 库将返回的 Markdown 字符串解析为 HTML
        // 这能正确处理标题、列表、加粗等所有标准格式
        resultContainer.innerHTML = marked.parse(data.outline);

    } catch (error) {
        console.error("请求失败:", error);
        resultContainer.innerHTML = `<p class="result-error">生成失败: ${error.message}</p>`;
    } finally {
        generateBtn.disabled = false;
        statusDisplay.classList.add('status-hidden');
        outputPanel.classList.remove('is-thinking'); // [新增] 请求结束后停止动画
    }
});