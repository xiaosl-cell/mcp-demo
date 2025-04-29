from dotenv import load_dotenv
import os
from openai import OpenAI  # 导入OpenAI官方库


# 加载环境变量
load_dotenv()

class LLMClient:
    def __init__(self):
        # 从环境变量获取API密钥和基础URL
        self.api_key = os.getenv("LLM_API_KEY")  # 使用OPENAI_API_KEY环境变量
        self.base_url = os.getenv("LLM_BASE_URL")  # 可选的API基础URL
        self.model = os.getenv("MODEL", "gpt-4o")  # 默认使用gpt-4o模型

        # 初始化OpenAI客户端
        if self.base_url:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        else:
            self.client = OpenAI(api_key=self.api_key)

        if not self.api_key:
            print("警告: 未设置LLM_API_KEY环境变量")
        if not self.model:
            print("警告: 未设置MODEL环境变量，将使用默认的gpt-4o模型")

    def ask(self, messages):
        """向OpenAI发送请求并获取响应"""
        if not self.api_key:
            return "未配置OpenAI API，请设置LLM_API_KEY环境变量"

        try:
            # 使用OpenAI官方库发送请求
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2,
                max_tokens=1000
            )
            # 返回生成的内容
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API调用失败: {e}")
            return f"API调用失败: {str(e)}"