import os
import subprocess
from you_get import common as you_get

def download_video(bv_number):
    """
    下载B站视频
    :param bv_number: 视频的BV号
    :return: 下载的视频文件路径
    """
    # 创建保存目录
    save_dir = "bilibili_video"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # 构建视频URL
    url = f"https://www.bilibili.com/video/BV{bv_number}"
    
    try:
        # 使用you-get下载视频
        you_get.download(
            url,
            output_dir=save_dir,
            output_filename=f"BV{bv_number}",
            merge=True
        )
        
        # 返回下载的文件路径
        return os.path.join(save_dir, f"BV{bv_number}.mp4")
    except Exception as e:
        print(f"下载视频时出错: {str(e)}")
        return None 