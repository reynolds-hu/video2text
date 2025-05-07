import os
from moviepy.editor import VideoFileClip
import librosa
import soundfile as sf

def process_audio_split(filename):
    """
    从视频中提取音频并分割
    :param filename: 视频文件路径
    :return: 处理后的音频文件夹名
    """
    try:
        # 创建输出目录
        output_dir = filename.replace('.mp4', '')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 从视频中提取音频
        video = VideoFileClip(filename)
        audio = video.audio
        audio_path = os.path.join(output_dir, "audio.mp3")
        audio.write_audiofile(audio_path)
        
        # 加载音频文件
        y, sr = librosa.load(audio_path)
        
        # 使用librosa进行音频分割（这里使用简单的静音检测）
        intervals = librosa.effects.split(y, top_db=20)
        
        # 保存分割后的音频片段
        for i, (start, end) in enumerate(intervals):
            segment = y[start:end]
            segment_path = os.path.join(output_dir, f"segment_{i:03d}.wav")
            sf.write(segment_path, segment, sr)
        
        # 清理临时文件
        audio.close()
        video.close()
        os.remove(audio_path)
        
        return output_dir
    except Exception as e:
        print(f"处理音频时出错: {str(e)}")
        return None 