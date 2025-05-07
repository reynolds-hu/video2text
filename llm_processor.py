import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def process_with_llm(text, prompt):
    """
    使用DeepSeek API处理文本
    :param text: 要处理的文本
    :param prompt: 处理提示词
    :return: 处理后的文本
    """
    try:
        # 构建完整的提示词
        full_prompt = f"{prompt}\n\n原文：\n{text}"
        
        # 调用DeepSeek API
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY', 'free')}"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是一个专业的文本优化助手，擅长整理和优化文本内容。"},
                {"role": "user", "content": full_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 4000
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 检查响应状态
        
        # 返回处理后的文本
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
        
    except Exception as e:
        error_msg = str(e)
        print(f"LLM处理文本时出错: {error_msg}")
        return text  # 如果处理失败，返回原始文本 