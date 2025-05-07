import os
import json
import time
import hmac
import base64
import hashlib
import websocket
from datetime import datetime
from urllib.parse import urlencode
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 错误码说明
ERROR_CODES = {
    "0": "成功",
    "10007": "用户流量受限：服务正在处理用户当前的问题，需等待处理完成后再发送新的请求。",
    "10013": "输入内容审核不通过，涉嫌违规，请重新调整输入内容",
    "10014": "输出内容涉及敏感信息，审核不通过，后续结果无法展示给用户",
    "10019": "本次会话内容有涉及违规信息的倾向",
    "10907": "token数量超过上限。对话历史+问题的字数太多，需要精简输入",
    "11200": "授权错误：该appId没有相关功能的授权 或者 业务量超过限制",
    "11201": "授权错误：日流控超限。超过当日最大访问量的限制",
    "11202": "授权错误：秒级流控超限。秒级并发超过授权路数限制",
    "11203": "授权错误：并发流控超限。并发路数超过授权路数限制"
}

class SparkAPI:
    def __init__(self):
        self.appid = os.getenv("SPARK_APPID", "")
        self.api_key = os.getenv("SPARK_API_KEY", "")
        self.api_secret = os.getenv("SPARK_API_SECRET", "")
        self.spark_url = "wss://spark-api.xf-yun.com/v1/x1"
        
        # 检查环境变量是否正确加载
        if not all([self.appid, self.api_key, self.api_secret]):
            print("警告：部分API密钥未正确加载，请检查.env文件")
            print(f"APPID: {self.appid}")
            print(f"API Key: {self.api_key[:4]}...{self.api_key[-4:] if self.api_key else ''}")
            print(f"API Secret: {self.api_secret[:4]}...{self.api_secret[-4:] if self.api_secret else ''}")
        
    def _create_url(self):
        """生成鉴权url"""
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
        
        # 拼接字符串
        signature_origin = f"host: spark-api.xf-yun.com\ndate: {date}\nGET /v1/x1 HTTP/1.1"
        
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(
            self.api_secret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        
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
        url = self.spark_url + '?' + urlencode(v)
        
        # 打印调试信息（不包含完整密钥）
        print("Debug - 签名信息:")
        print(f"Date: {date}")
        print(f"Signature Origin: {signature_origin}")
        print(f"Authorization Origin: {authorization_origin}")
        print(f"URL (部分): {url[:100]}...")
        
        return url

    def process_text(self, text, prompt):
        """处理文本"""
        try:
            # 构建完整的提示词
            full_prompt = f"{prompt}\n\n原文：\n{text}"
            
            # 构建请求数据
            data = {
                "header": {
                    "app_id": self.appid,
                    "uid": "user_001"
                },
                "parameter": {
                    "chat": {
                        "domain": "x1",
                        "temperature": 0.5,
                        "max_tokens": 4096,
                        "presence_penalty": 1,
                        "frequency_penalty": 0.02,
                        "top_k": 5,
                        "tools": [
                            {
                                "type": "web_search",
                                "web_search": {
                                    "enable": True,
                                    "search_mode": "normal"
                                }
                            }
                        ]
                    }
                },
                "payload": {
                    "message": {
                        "text": [
                            {
                                "role": "system",
                                "content": "你是一个专业的文本优化助手，擅长整理和优化文本内容。"
                            },
                            {
                                "role": "user",
                                "content": full_prompt
                            }
                        ]
                    }
                }
            }
            
            # 创建WebSocket连接
            ws = websocket.create_connection(self._create_url())
            
            # 发送数据
            ws.send(json.dumps(data))
            
            # 接收响应
            response = ws.recv()
            ws.close()
            
            # 解析响应
            result = json.loads(response)
            if "payload" in result and "choices" in result["payload"]:
                return result["payload"]["choices"]["text"][0]["content"].strip()
            else:
                return text
                
        except Exception as e:
            error_msg = str(e)
            print(f"LLM处理文本时出错: {error_msg}")
            
            # 尝试解析错误信息
            try:
                if "401" in error_msg:
                    print("错误码: 401 Unauthorized")
                    print("可能的原因:")
                    print("1. API密钥不正确")
                    print("2. 签名生成有误")
                    print("3. 时间戳过期")
                elif "message" in error_msg:
                    error_json = json.loads(error_msg.split("b'")[1].rstrip("'"))
                    if "message" in error_json:
                        print(f"错误信息: {error_json['message']}")
            except:
                pass
                
            return text

# 创建全局实例
spark_api = SparkAPI()

def process_with_llm(text, prompt):
    """全局处理函数"""
    return spark_api.process_text(text, prompt) 