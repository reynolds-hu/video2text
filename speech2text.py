import os
import whisper
import torch

class WhisperModel:
    def __init__(self):
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    def load_whisper(self, model="small"):
        """
        加载Whisper模型
        :param model: 模型大小，可选 "tiny", "base", "small", "medium", "large"
        """
        try:
            self.model = whisper.load_model(model, device=self.device)
            print(f"Whisper模型 {model} 加载成功！使用设备: {self.device}")
        except Exception as e:
            print(f"加载Whisper模型时出错: {str(e)}")
    
    def run_analysis(self, foldername, prompt="以下是普通话的句子。"):
        """
        分析音频文件并生成文本
        :param foldername: 音频文件夹路径
        :param prompt: 提示词
        :return: 生成的文本文件路径
        """
        if self.model is None:
            print("请先加载Whisper模型！")
            return None
        
        try:
            # 创建输出目录
            output_dir = "outputs"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 获取所有音频文件
            audio_files = sorted([f for f in os.listdir(foldername) if f.endswith('.wav')])
            
            # 存储所有文本
            all_text = []
            
            # 处理每个音频文件
            for audio_file in audio_files:
                audio_path = os.path.join(foldername, audio_file)
                result = self.model.transcribe(
                    audio_path,
                    language="zh",
                    initial_prompt=prompt
                )
                all_text.append(result["text"])
            
            # 保存结果
            output_path = os.path.join(output_dir, f"{os.path.basename(foldername)}.txt")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("\n".join(all_text))
            
            return output_path
        except Exception as e:
            print(f"分析音频时出错: {str(e)}")
            return None

# 创建全局实例
whisper_model = WhisperModel()

def load_whisper(model="small"):
    """全局加载函数"""
    whisper_model.load_whisper(model)

def run_analysis(foldername, prompt="以下是普通话的句子。"):
    """全局分析函数"""
    return whisper_model.run_analysis(foldername, prompt) 