import os
import requests
import json
import time
import hmac
import base64
import hashlib
from datetime import datetime
from urllib.parse import urlparse
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class SparkAPI:
    def __init__(self):
        self.appid = os.getenv("SPARK_APPID", "")
        self.api_key = os.getenv("SPARK_API_KEY", "")
        self.api_secret = os.getenv("SPARK_API_SECRET", "")
        self.spark_url = "wss://spark-api.xf-yun.com/v3.1/chat"
        
    def _create_url(self):
        """生成鉴权url"""
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
        
        # 拼接字符串
        signature_origin = f"host: spark-api.xf-yun.com\ndate: {date}\nGET /v3.1/chat HTTP/1.1"
        
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.api_secret.encode('utf-8'), 
                               signature_origin.encode('utf-8'),
                               digestmod=hashlib.sha256).digest()
        
        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')
        
        authorization_origin = f'api_key="{self.api_key}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
        
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "spark-api.xf-yun.com"
        }
        # 拼接鉴权参数，生成url
        url = self.spark_url + '?' + urlparse.urlencode(v)
        return url

    def process_text(self, text, prompt):
        """处理文本"""
        try:
            # 构建完整的提示词
            full_prompt = f"{prompt}\n\n原文：\n{text}"
            
            # 构建请求数据
            data = {
                "header": {
                    "app_id": self.appid
                },
                "parameter": {
                    "chat": {
                        "domain": "general",
                        "temperature": 0.7,
                        "max_tokens": 4000
                    }
                },
                "payload": {
                    "message": {
                        "text": [
                            {"role": "system", "content": "你是一个专业的文本优化助手，擅长整理和优化文本内容。"},
                            {"role": "user", "content": full_prompt}
                        ]
                    }
                }
            }
            
            # 发送请求
            response = requests.post(
                self._create_url(),
                json=data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            if "payload" in result and "message" in result["payload"]:
                return result["payload"]["message"]["text"][0]["content"].strip()
            else:
                return text
                
        except Exception as e:
            error_msg = str(e)
            print(f"LLM处理文本时出错: {error_msg}")
            return text

# 创建全局实例
spark_api = SparkAPI()

def process_with_llm(text, prompt):
    """全局处理函数"""
    return spark_api.process_text(text, prompt) 