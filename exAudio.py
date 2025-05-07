import os
from moviepy.editor import VideoFileClip
import librosa
import soundfile as sf
import numpy as np

def extract_audio(video_path, output_dir=None):
    """
    从视频中提取音频
    :param video_path: 视频文件路径
    :param output_dir: 输出目录，默认为None（使用视频所在目录）
    :return: 提取的音频文件路径
    """
    if not video_path or not os.path.exists(video_path):
        print(f"错误：视频文件不存在 - {video_path}")
        return None
        
    try:
        # 如果未指定输出目录，使用项目目录下的temp_videos
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(__file__), "temp_videos")
            
        # 确保输出目录存在
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # 生成输出文件路径
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        audio_path = os.path.join(output_dir, f"{video_name}.wav")
        
        # 加载视频文件
        video = VideoFileClip(video_path)
        
        # 提取音频
        audio = video.audio
        
        # 保存音频文件
        audio.write_audiofile(audio_path)
        
        # 关闭视频和音频对象
        audio.close()
        video.close()
        
        return audio_path
        
    except Exception as e:
        print(f"提取音频时出错: {str(e)}")
        return None

def process_audio_split(filename, min_segment_length=30, max_segment_length=300):
    """
    从视频中提取音频并分割
    :param filename: 视频文件路径
    :param min_segment_length: 最小片段长度（秒）
    :param max_segment_length: 最大片段长度（秒）
    :return: 处理后的音频文件夹名
    """
    try:
        # 创建输出目录（使用项目目录下的temp_videos）
        base_dir = os.path.dirname(__file__)
        output_dir = os.path.join(base_dir, "temp_videos", os.path.splitext(os.path.basename(filename))[0])
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 从视频中提取音频
        video = VideoFileClip(filename)
        audio = video.audio
        audio_path = os.path.join(output_dir, "audio.mp3")
        audio.write_audiofile(audio_path)
        
        # 加载音频文件
        y, sr = librosa.load(audio_path)
        
        # 使用librosa进行音频分割（使用更长的静音检测阈值）
        intervals = librosa.effects.split(y, top_db=25, frame_length=2048, hop_length=512)
        
        # 合并太短的片段
        merged_intervals = []
        current_start = intervals[0][0]
        current_end = intervals[0][1]
        
        for start, end in intervals[1:]:
            # 计算当前片段长度（秒）
            current_length = (current_end - current_start) / sr
            next_length = (end - start) / sr
            
            # 如果当前片段太短，尝试合并
            if current_length < min_segment_length:
                current_end = end
            # 如果当前片段太长，需要分割
            elif current_length > max_segment_length:
                # 保存当前片段
                merged_intervals.append((current_start, current_end))
                # 开始新片段
                current_start = start
                current_end = end
            else:
                # 保存当前片段
                merged_intervals.append((current_start, current_end))
                # 开始新片段
                current_start = start
                current_end = end
        
        # 添加最后一个片段
        merged_intervals.append((current_start, current_end))
        
        # 保存分割后的音频片段
        for i, (start, end) in enumerate(merged_intervals):
            segment = y[start:end]
            segment_path = os.path.join(output_dir, f"segment_{i:03d}.wav")
            sf.write(segment_path, segment, sr)
        
        # 清理临时文件
        audio.close()
        video.close()
        os.remove(audio_path)
        
        print(f"音频已分割为 {len(merged_intervals)} 个片段")
        return output_dir
    except Exception as e:
        print(f"处理音频时出错: {str(e)}")
        return None 