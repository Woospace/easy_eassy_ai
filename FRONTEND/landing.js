// landing.js (Firebase Module Version)

// 1. 从 Firebase CDN 引入所有需要的函数。
//    这使得所有逻辑都集中在本文件，更易于管理。
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.10/firebase-app.js";
import { getAuth, GoogleAuthProvider, signInWithPopup } from "https://www.gstatic.com/firebasejs/9.6.10/firebase-auth.js";

// 2. 你的 Firebase 项目配置信息
const firebaseConfig = {
    apiKey: "AIzaSyDyCf4m4dJIHiA5Nl5Npq5RPU074J4BVXg",
    authDomain: "easy-essay-ai.firebaseapp.com",
    projectId: "easy-essay-ai",
    storageBucket: "easy-essay-ai.firebasestorage.app",
    messagingSenderId: "232184426587",
    appId: "1:232184426587:web:6120d04d419d7d552ecf7e"
};

// 3. 初始化 Firebase 应用和认证服务
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider(); // 创建 Google 登录提供程序

// --- 主逻辑 ---

// 确保在 DOM 完全加载后再执行脚本
document.addEventListener('DOMContentLoaded', () => {
    // 获取页面上的按钮和错误信息元素
    const loginButton = document.getElementById('google-login-btn');
    const errorMessage = document.getElementById('error-message');

    // 为“Google 登录”按钮绑定点击事件
    loginButton.addEventListener('click', async () => {
        errorMessage.textContent = ''; // 点击时清空旧的错误信息

        try {
            // 步骤 A: 弹出 Google 登录窗口并等待用户操作
            const result = await signInWithPopup(auth, provider);
            const user = result.user;

            // 步骤 B: 从成功登录的用户信息中获取 ID Token
            const idToken = await user.getIdToken();

            // 步骤 C: 将 ID Token 发送到后端进行安全验证
            const response = await fetch('/google-login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ token: idToken })
            });

            const data = await response.json();

            // 步骤 D: 根据后端的响应进行后续操作
            if (response.ok && data.success) {
                // 如果后端确认用户有效，则跳转到主页面
                window.location.href = '/index';
            } else {
                // 如果后端返回错误，则抛出异常
                throw new Error(data.error || '后端验证失败。');
            }

        } catch (error) {
            // 统一处理登录过程中发生的任何错误（如网络问题、用户关闭弹窗等）
            console.error('登录流程失败:', error);
            errorMessage.textContent = '登录失败或用户取消。';
        }
    });
});