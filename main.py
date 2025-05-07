from downBili import download_video, extract_bv_number, cleanup_video
# from downYT import download_youtube_video
from exAudio import process_audio_split
from speech2text import load_whisper, run_analysis
from llm_processor import process_with_llm
import os

def main():
    url = input("请输入B站视频URL：")
    bv_number = extract_bv_number(url)
    if bv_number:
        filename = download_video(bv_number[2:])
        if filename:
            try:
                # 1. 处理音频
                print("正在处理音频...")
                foldername = process_audio_split(filename)
                
                # 2. 语音转文字
                print("正在转换语音为文字...")
                load_whisper("small")
                raw_text_path = run_analysis(foldername, prompt="以下是普通话的句子。")
                
                # 3. LLM处理文本
                print("正在使用LLM优化文本...")
                if raw_text_path and os.path.exists(raw_text_path):
                    # 读取原始文本
                    with open(raw_text_path, 'r', encoding='utf-8') as f:
                        raw_text = f.read()
                    
                    # 使用LLM处理文本
                    prompt = """请对以下文本进行优化处理：
                            1. 删除重复、无意义的内容
                            2. 保持专业术语和重要信息的完整性
                            3. 优化语言表达，使其更加通顺
                            4. 保持段落结构，便于阅读
                            5. 保留所有关键信息和数据

                            请直接输出优化后的文本，不要添加任何额外的说明或标记。"""
                    
                    processed_text = process_with_llm(raw_text, prompt)
                    
                    # 保存处理后的文本
                    output_dir = os.path.join(os.path.dirname(__file__), "outputs")
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    
                    output_path = os.path.join(output_dir, f"{os.path.basename(foldername)}_processed.txt")
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(processed_text)
                    
                    print(f"处理完成！输出文件：{output_path}")
                else:
                    print("文本处理失败！")
            finally:
                # 处理完成后清理视频文件
                cleanup_video(filename)
        else:
            print("下载视频失败！")
    else:
        print("无法从URL中提取BV号！")

if __name__ == "__main__":
    main() 