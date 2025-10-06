# llm_service.py (v3 - No File I/O)

from openai import OpenAI
# 直接从 config 导入所有需要的变量，包括 SYSTEM_PROMPT
from config import YOUR_LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, SYSTEM_PROMPT

class LLMService:
    def __init__(self):
        # 1. 初始化LLM客户端
        self.client = OpenAI(api_key=YOUR_LLM_API_KEY, base_url=LLM_BASE_URL)
        
        # 2. 直接从配置模块获取Prompt模板，不再执行文件读取操作
        #    这让服务启动更快，也更符合“配置与代码分离”的原则
        self.prompt_template = SYSTEM_PROMPT
        print("--- LLMService: Prompt 模板已从环境变量成功加载 ---")

    def generate_outline(self, subject: str, requirements: str, rubric: str) -> str:
        """
        根据学科、作业要求和评分标准，生成结构化的大纲。
        """
        # 1. 动态填充Prompt模板 (逻辑不变)
        #    注意：请确保你的 .env 文件中的 SYSTEM_PROMPT 包含 [学科] 这个占位符
        prompt_with_subject = self.prompt_template.replace(
            "[学科]", subject
        )
        final_prompt = prompt_with_subject.replace(
            "[此处将粘贴用户输入的作业要求]", requirements
        ).replace(
            "[此处将粘贴用户输入的评分标准]", rubric
        )
        
        # 2. 调用LLM API (逻辑不变)
        try:
            response = self.client.chat.completions.create(
                model=LLM_MODEL,
                messages=[{"role": "user", "content": final_prompt}],
            )
            outline = response.choices[0].message.content
            usage = response.usage
            print(f"--- Token Usage: Prompt={usage.prompt_tokens}, Completion={usage.completion_tokens}, Total={usage.total_tokens} ---")
            
            return outline
        except Exception as e:
            print(f"调用LLM API时发生错误: {e}")
            raise
        
# 创建一个全局单例
llm_service = LLMService()
