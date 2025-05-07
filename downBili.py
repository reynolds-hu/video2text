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
        return match.group(0)
    return None

def download_video(bv_number):
    """
    下载B站视频
    :param bv_number: 视频的BV号
    :return: 下载的视频文件路径
    """
    # 创建临时目录
    temp_dir = "temp_videos"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    # 构建视频URL和文件路径
    url = f"https://www.bilibili.com/video/BV{bv_number}"
    video_path = os.path.join(temp_dir, f"BV{bv_number}.mp4")
    
    try:
        # 使用you-get命令行工具下载视频
        subprocess.run(["you-get", url, "-o", temp_dir], check=True)
        return video_path
    except subprocess.CalledProcessError as e:
        print(f"下载视频时出错: {str(e)}")
        return None

def cleanup_video(video_path):
    """
    清理下载的视频文件
    :param video_path: 视频文件路径
    """
    if os.path.exists(video_path):
        os.remove(video_path)
        # 如果临时目录为空，也删除它
        temp_dir = os.path.dirname(video_path)
        if not os.listdir(temp_dir):
            os.rmdir(temp_dir) 