from downBili import download_video
# from downYT import download_youtube_video
from exAudio import process_audio_split
from speech2text import load_whisper, run_analysis
# from llm_processor import process_with_llm

def main():
    # video_type = input("请选择视频类型 (1: Bilibili, 2: YouTube): ")
    # if video_type == "1":
    av = input("请输入BV号：")
    filename = download_video(av[2:])
    # elif video_type == "2":
    #     url = input("请输入YouTube视频URL：")
    #     filename = download_youtube_video(url)
    # else:
    #     print("无效的选择！")
    #     return

    if filename:
        foldername = process_audio_split(filename)
        load_whisper("small")
        run_analysis(foldername, prompt="以下是普通话的句子。")
        output_path = f"outputs/{foldername}.txt"
        print("转换完成！", output_path)

        # 使用LLM处理文本
        # with open(output_path, 'r', encoding='utf-8') as file:
        #     text_content = file.read()
        # processed_text = process_with_llm(text_content)
        # print("LLM处理完成！", processed_text)
    else:
        print("下载视频失败！")

if __name__ == "__main__":
    main() 