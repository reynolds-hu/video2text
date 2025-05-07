# Video to Text Converter

## 项目简介
这个项目用于将视频中的音频转换为文本。它支持从Bilibili下载视频，提取音频，使用Whisper模型将音频转换为文本，并使用LLM优化文本内容。

## 功能
- 从Bilibili下载视频
- 提取视频中的音频
- 使用Whisper模型将音频转换为文本
- 使用LLM优化和总结文本内容
- 智能音频分段处理
- GPU加速支持

## 使用方法
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 配置环境：
   - 创建 `.env` 文件并添加 OpenAI API 密钥：
     ```
     OPENAI_API_KEY=你的API密钥
     ```

3. 运行程序：
   ```bash
   python main.py
   ```

## 性能优化
- GPU加速：
  - 自动检测并使用GPU（如NVIDIA显卡）
  - 支持CUDA加速，显著提升处理速度
  - 实时显示GPU显存使用情况

- 音频处理优化：
  - 智能音频分段，避免过多小片段
  - 自动合并短片段（<30秒）
  - 自动分割长片段（>300秒）
  - 优化静音检测参数

- 文本处理优化：
  - 使用LLM优化文本内容
  - 删除重复内容
  - 保持专业术语完整性
  - 优化语言表达
  - 保持段落结构

## 系统要求
- Python 3.8+
- 足够的磁盘空间
- 推荐使用GPU（NVIDIA显卡）以获得更好的性能
- 如果使用GPU，需要安装CUDA和对应版本的PyTorch

## 注意事项
- 首次运行时会下载Whisper模型，可能需要一些时间
- 使用GPU时，建议使用支持CUDA的PyTorch版本
- 处理长视频时，建议使用GPU以获得更好的性能
- 确保有足够的磁盘空间存储临时文件和输出结果

## Project Description
This project is used to convert audio from videos into text. It supports downloading videos from Bilibili, extracting audio, using the Whisper model to convert audio into text, and optimizing the text content using LLM.

## Features
- Download videos from Bilibili
- Extract audio from videos
- Convert audio to text using the Whisper model
- Optimize and summarize text content using LLM
- Intelligent audio segmentation
- GPU acceleration support

## Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment:
   - Create `.env` file and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key
     ```

3. Run the program:
   ```bash
   python main.py
   ```

## Performance Optimizations
- GPU Acceleration:
  - Automatic GPU detection and utilization
  - CUDA support for significant speed improvement
  - Real-time GPU memory usage monitoring

- Audio Processing Optimization:
  - Intelligent audio segmentation
  - Automatic short segment merging (<30s)
  - Automatic long segment splitting (>300s)
  - Optimized silence detection parameters

- Text Processing Optimization:
  - LLM-based text optimization
  - Duplicate content removal
  - Professional terminology preservation
  - Language expression improvement
  - Paragraph structure maintenance

## System Requirements
- Python 3.8+
- Sufficient disk space
- GPU recommended (NVIDIA graphics card) for better performance
- CUDA and corresponding PyTorch version if using GPU

## Notes
- First run will download the Whisper model, which may take some time
- When using GPU, it's recommended to use PyTorch with CUDA support
- For long videos, GPU is recommended for better performance
- Ensure sufficient disk space for temporary files and output results 
