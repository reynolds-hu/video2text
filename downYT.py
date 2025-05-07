import os
from pytube import YouTube

def download_youtube_video(url):
    """
    下载YouTube视频
    :param url: YouTube视频的URL
    :return: 下载的视频文件路径
    """
    # 创建保存目录
    save_dir = "youtube_video"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    try:
        # 使用pytube下载视频
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        video_path = video.download(output_path=save_dir)
        
        return video_path
    except Exception as e:
        print(f"下载YouTube视频时出错: {str(e)}")
        return None 