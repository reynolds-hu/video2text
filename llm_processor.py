import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化OpenAI客户端
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def process_with_llm(text, prompt):
    """
    使用LLM处理文本
    :param text: 要处理的文本
    :param prompt: 处理提示词
    :return: 处理后的文本
    """
    try:
        # 构建完整的提示词
        full_prompt = f"{prompt}\n\n原文：\n{text}"
        
        # 调用OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",  # 使用支持更长文本的模型
            messages=[
                {"role": "system", "content": "你是一个专业的文本优化助手，擅长整理和优化文本内容。"},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7,  # 适当调整创造性
            max_tokens=4000,  # 设置较大的输出限制
        )
        
        # 返回处理后的文本
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"LLM处理文本时出错: {str(e)}")
        return text  # 如果处理失败，返回原始文本 