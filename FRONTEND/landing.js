// FilePath: frontend/landing.js

document.addEventListener('DOMContentLoaded', () => {
    const accessForm = document.getElementById('access-form');
    const accessCodeInput = document.getElementById('access-code');
    const errorMessage = document.getElementById('error-message');

    accessForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // 阻止表单默认的提交行为
        
        const code = accessCodeInput.value.trim();
        errorMessage.textContent = ''; // 清空之前的错误信息

        if (!code) {
            errorMessage.textContent = '请输入访问码。';
            return;
        }

        try {
            const response = await fetch('/verify_code', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ code: code })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                // 验证成功，跳转到主应用页面
                window.location.href = '/index';
            } else {
                // 验证失败，显示错误信息
                errorMessage.textContent = data.error || '验证失败，请重试。';
                accessCodeInput.value = ''; // 清空输入框
            }

        } catch (error) {
            console.error('验证请求失败:', error);
            errorMessage.textContent = '请求失败，请检查网络连接。';
        }
    });
});