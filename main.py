from downBili import download_video, extract_bv_number, cleanup_video
# from downYT import download_youtube_video
from exAudio import process_audio_split
from speech2text import load_whisper, run_analysis
# from llm_processor import process_with_llm
import os

def main():
    url = input("请输入B站视频URL：")
    bv_number = extract_bv_number(url)
    if bv_number:
        filename = download_video(bv_number[2:])
        if filename:
            try:
                foldername = process_audio_split(filename)
                load_whisper("small")
                run_analysis(foldername, prompt="以下是普通话的句子。")
                output_path = f"outputs/{foldername}.txt"
                print("转换完成！", output_path)
            finally:
                # 处理完成后清理视频文件
                cleanup_video(filename)
        else:
            print("下载视频失败！")
    else:
        print("无法从URL中提取BV号！")

if __name__ == "__main__":
    main() 