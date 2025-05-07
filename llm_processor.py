from openai import OpenAI

def process_with_llm(text_content):
    """
    使用大语言模型处理文本
    """
    client = OpenAI()
    
    # 构建提示词
    prompt = f"""
    请将以下字幕内容进行美化和结构化处理：
    1. 删除重复内容
    2. 合并相似内容
    3. 添加适当的段落和标题
    4. 优化语言表达
    
    字幕内容：
    {text_content}
    """
    
    # 调用API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一个专业的文本编辑助手"},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content 