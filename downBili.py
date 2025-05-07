import re
import subprocess
import os
import shutil

def extract_bv_number(url):
    """
    从B站视频URL中提取BV号
    :param url: B站视频的完整URL
    :return: 提取的BV号
    """
    match = re.search(r'BV([A-Za-z0-9]+)', url)
    if match:
        return match.group(0)  # 返回完整的BV号（包含BV前缀）
    return None

def download_video(bv_number):
    """
    下载B站视频
    :param bv_number: 视频的BV号（包含BV前缀）
    :return: 下载的视频文件路径
    """
    try:
        # 创建临时目录
        temp_dir = os.path.join(os.path.dirname(__file__), "temp_videos")
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        # 确保bv_number包含BV前缀
        if not bv_number.startswith('BV'):
            bv_number = f'BV{bv_number}'
        
        # 构建视频URL和文件路径
        url = f"https://www.bilibili.com/video/{bv_number}"
        video_path = os.path.join(temp_dir, f"{bv_number}.mp4")
        
        print(f"正在下载视频: {url}")
        print(f"保存到: {video_path}")
        
        # 使用you-get命令行工具下载视频
        subprocess.run(["you-get", url, "-o", temp_dir], check=True)
        
        # 检查文件是否存在
        if os.path.exists(video_path):
            return video_path
        else:
            # 如果文件不存在，尝试在temp_dir中查找下载的文件
            files = os.listdir(temp_dir)
            for file in files:
                if file.endswith('.mp4'):
                    return os.path.join(temp_dir, file)
            
            print(f"警告：未找到下载的视频文件")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"下载视频时出错: {str(e)}")
        return None
    except Exception as e:
        print(f"发生未知错误: {str(e)}")
        return None

def cleanup_video(video_path):
    """
    清理下载的视频文件
    :param video_path: 视频文件路径
    """
    if video_path and os.path.exists(video_path):
        try:
            os.remove(video_path)
            # 如果临时目录为空，也删除它
            temp_dir = os.path.dirname(video_path)
            if not os.listdir(temp_dir):
                os.rmdir(temp_dir)
        except Exception as e:
            print(f"清理视频文件时出错: {str(e)}") 