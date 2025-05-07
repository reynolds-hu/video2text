import os
import whisper
import torch
import platform

class WhisperModel:
    def __init__(self):
        self.model = None
        self.device = self._get_device()
    
    def _get_device(self):
        """
        检测并返回可用的设备
        """
        if torch.cuda.is_available():
            # 获取GPU信息
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3  # 转换为GB
            print(f"检测到GPU: {gpu_name}")
            print(f"GPU显存: {gpu_memory:.1f}GB")
            return "cuda"
        else:
            print("未检测到GPU，将使用CPU")
            print(f"系统信息: {platform.platform()}")
            return "cpu"
    
    def load_whisper(self, model="small"):
        """
        加载Whisper模型
        :param model: 模型大小，可选 "tiny", "base", "small", "medium", "large"
        """
        try:
            print(f"正在加载Whisper模型 {model}...")
            self.model = whisper.load_model(model, device=self.device)
            print(f"Whisper模型 {model} 加载成功！使用设备: {self.device}")
            
            # 如果使用GPU，显示显存使用情况
            if self.device == "cuda":
                allocated = torch.cuda.memory_allocated() / 1024**3
                reserved = torch.cuda.memory_reserved() / 1024**3
                print(f"GPU显存使用: {allocated:.1f}GB (已分配) / {reserved:.1f}GB (已保留)")
                
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
            output_dir = os.path.join(os.path.dirname(__file__), "outputs")
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 获取所有音频文件
            audio_files = sorted([f for f in os.listdir(foldername) if f.endswith('.wav')])
            total_files = len(audio_files)
            
            # 存储所有文本
            all_text = []
            
            # 处理每个音频文件
            for i, audio_file in enumerate(audio_files, 1):
                print(f"正在处理音频文件 {i}/{total_files}: {audio_file}")
                audio_path = os.path.join(foldername, audio_file)
                result = self.model.transcribe(
                    audio_path,
                    language="zh",
                    initial_prompt=prompt
                )
                all_text.append(result["text"])
                
                # 如果使用GPU，显示显存使用情况
                if self.device == "cuda":
                    allocated = torch.cuda.memory_allocated() / 1024**3
                    print(f"当前GPU显存使用: {allocated:.1f}GB")
            
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