#!/usr/bin/env python3
"""
将 modelverse 文档从 docsify 格式转换为 Nextra 格式
"""

import os
import re
import json
import shutil
from pathlib import Path

SOURCE_DIR = "modelverse"
TARGET_DIR = "modelverse_new"

def convert_links_in_content(content):
    """转换文档内容中的链接格式"""
    # 将 /modelverse/xxx.md 转换为相对路径
    def replace_link(match):
        text = match.group(1)
        path = match.group(2)
        # 移除 /modelverse/ 前缀
        path = re.sub(r'^/modelverse/', '/', path)
        # 移除 .md 后缀
        path = re.sub(r'\.md$', '', path)
        return f'[{text}]({path})'
    
    content = re.sub(r'\[([^\]]+)\]\((/modelverse/[^\)]+)\)', replace_link, content)
    return content

def copy_and_convert_file(src_path, dst_path):
    """复制并转换单个文件"""
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    
    if src_path.suffix.lower() in ['.md', '.mdx']:
        with open(src_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = convert_links_in_content(content)
        with open(dst_path, 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        shutil.copy2(src_path, dst_path)

def generate_meta_json(meta_dict, output_path):
    """生成 _meta.json 文件"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(meta_dict, f, ensure_ascii=False, indent=2)

def main():
    source = Path(SOURCE_DIR)
    target = Path(TARGET_DIR)
    
    # 清理目标目录
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    
    # 复制所有文件（排除 _sidebar.md 和隐藏文件/目录）
    for src_file in source.rglob('*'):
        # 跳过隐藏文件和目录（如 .git, .DS_Store, .gitignore）
        rel_path = src_file.relative_to(source)
        if any(part.startswith('.') for part in rel_path.parts):
            continue
        if not src_file.is_file():
            continue
        if src_file.name == '_sidebar.md':
            continue
            
        # 将 README.md 重命名为 index.md
        if rel_path.name == 'README.md':
            rel_path = rel_path.parent / 'index.md'
        
        dst_file = target / rel_path
        copy_and_convert_file(src_file, dst_file)
        print(f"已转换: {src_file} -> {dst_file}")
    
    # 生成各级目录的 _meta.json
    
    # 根目录 _meta.json
    root_meta = {
        "index": "概览",
        "introduction": "产品简介",
        "price": "计费说明",
        "api_doc": "API 调用",
        "best_practice": "最佳实践",
        "guide": "操作指南",
        "private": "隐私政策"
    }
    generate_meta_json(root_meta, target / '_meta.json')
    print(f"已生成: {target / '_meta.json'}")
    
    # introduction 目录
    intro_meta = {
        "introduction": "什么是模型服务平台",
        "advantages": "产品优势"
    }
    generate_meta_json(intro_meta, target / 'introduction' / '_meta.json')
    print(f"已生成: {target / 'introduction' / '_meta.json'}")
    
    # api_doc 目录
    api_meta = {
        "quick-start": "快速开始",
        "common": "通用说明",
        "text_api": "文本生成",
        "image_api": "图片生成",
        "video_api": "视频生成",
        "audio_api": "音频生成",
        "qa": "常见问题答疑"
    }
    generate_meta_json(api_meta, target / 'api_doc' / '_meta.json')
    print(f"已生成: {target / 'api_doc' / '_meta.json'}")
    
    # api_doc/common 目录
    common_meta = {
        "certificate": "认证鉴权",
        "error-code": "错误码"
    }
    generate_meta_json(common_meta, target / 'api_doc' / 'common' / '_meta.json')
    print(f"已生成: {target / 'api_doc' / 'common' / '_meta.json'}")
    
    # api_doc/text_api 目录
    text_meta = {
        "models": "如何获取模型列表",
        "model-competi": "模型协议支持说明",
        "api-expand": "API支持与UCloud扩展字段说明",
        "openai_compatible": "OpenAI Chat Completions 说明",
        "response_api": "OpenAI Response API 说明",
        "embeddings": "Embeddings 向量嵌入",
        "deepseek-ocr": "DeepSeek-OCR 模型调用示例",
        "struct": "OpenAI 文本接口结构说明",
        "thinking": "思考模式",
        "gemini_compatible": "Gemini 快速开始",
        "claude_compatible": "Claude (Anthropic) 兼容说明"
    }
    generate_meta_json(text_meta, target / 'api_doc' / 'text_api' / '_meta.json')
    print(f"已生成: {target / 'api_doc' / 'text_api' / '_meta.json'}")
    
    # api_doc/text_api/thinking 目录
    thinking_meta = {
        "deepseek": "DeepSeek 思考模式",
        "doubao": "Doubao 豆包模型思考开关"
    }
    generate_meta_json(thinking_meta, target / 'api_doc' / 'text_api' / 'thinking' / '_meta.json')
    print(f"已生成: {target / 'api_doc' / 'text_api' / 'thinking' / '_meta.json'}")
    
    # api_doc/image_api 目录
    image_meta = {
        "gemini-2.5-flash-image": "gemini-2.5-flash-image (Nano Banana)",
        "gemini-3-pro-image": "gemini-3-pro-image (Nano Banana 2)",
        "flux-2-pro": "flux-2-pro",
        "flux-kontext-pro": "flux-kontext-pro",
        "flux-pro-1.1": "flux-pro-1.1",
        "black-forest-labs-flux.1-dev": "black-forest-labs/flux.1-dev",
        "stepfun-ai-step1x-edit": "stepfun-ai/step1x-edit",
        "black-forest-labs-flux-kontext-max": "black-forest-labs/flux-kontext-max",
        "black-forest-labs-flux-kontext-max-multi": "black-forest-labs/flux-kontext-max/multi",
        "black-forest-labs-flux-kontext-max-text-to-image": "black-forest-labs/flux-kontext-max/text-to-image",
        "black-forest-labs-flux-kontext-pro": "black-forest-labs/flux-kontext-pro",
        "black-forest-labs-flux-kontext-pro-multi": "black-forest-labs/flux-kontext-pro/multi",
        "black-forest-labs-flux-kontext-pro-text-to-image": "black-forest-labs/flux-kontext-pro/text-to-image",
        "Qwen-Qwen-Image-Edit": "Qwen/Qwen-Image-Edit",
        "Qwen-Qwen-Image": "Qwen/Qwen-Image",
        "gpt-image-1": "gpt-image-1",
        "gpt-image-1.5": "gpt-image-1.5",
        "doubao-seedream-4.5": "doubao-seedream-4.5"
    }
    generate_meta_json(image_meta, target / 'api_doc' / 'image_api' / '_meta.json')
    print(f"已生成: {target / 'api_doc' / 'image_api' / '_meta.json'}")
    
    # api_doc/video_api 目录
    video_meta = {
        "OpenAI-Sora2-T2V": "OpenAI/Sora2-T2V",
        "OpenAI-Sora2-T2V-Pro": "OpenAI/Sora2-T2V-Pro",
        "OpenAI-Sora2-I2V": "OpenAI/Sora2-I2V",
        "OpenAI-Sora2-I2V-Pro": "OpenAI/Sora2-I2V-Pro",
        "Wan-AI-Wan2.2-I2V": "Wan-AI/Wan2.2-I2V",
        "Wan-AI-Wan2.2-T2V": "Wan-AI/Wan2.2-T2V",
        "Wan-AI-Wan2.5-I2V": "Wan-AI/Wan2.5-I2V",
        "Wan-AI-Wan2.5-T2V": "Wan-AI/Wan2.5-T2V",
        "Wan-AI-Wan2.6-I2V": "Wan-AI/Wan2.6-I2V",
        "Wan-AI-Wan2.6-T2V": "Wan-AI/Wan2.6-T2V",
        "vidu": "Vidu 系列",
        "doubao-seedance-1-5-pro-251215": "doubao-seedance-1-5-pro",
        "MiniMax-Hailuo-2.3-I2V": "MiniMax/Hailuo-2.3-I2V",
        "MiniMax-Hailuo-2.3-T2V": "MiniMax/Hailuo-2.3-T2V",
        "Kling-O1": "kling-video-o1",
        "Kling-v2.6-I2V": "kling-v2-6/图生视频",
        "Kling-v2.6-T2V": "kling-v2-6/文生视频",
        "Veo-3.1": "Veo-3.1/文图生视频"
    }
    generate_meta_json(video_meta, target / 'api_doc' / 'video_api' / '_meta.json')
    print(f"已生成: {target / 'api_doc' / 'video_api' / '_meta.json'}")
    
    # api_doc/video_api/vidu 目录
    vidu_meta = {
        "Vidu-Text2Video": "文生视频",
        "Vidu-Img2Video": "图生视频",
        "Vidu-Reference2Video": "参考图生视频",
        "Vidu-StartEnd2Video": "首尾帧生视频",
        "Vidu-Extend": "视频延长",
        "Vidu-LipSync": "对口型"
    }
    generate_meta_json(vidu_meta, target / 'api_doc' / 'video_api' / 'vidu' / '_meta.json')
    print(f"已生成: {target / 'api_doc' / 'video_api' / 'vidu' / '_meta.json'}")
    
    # api_doc/audio_api 目录
    audio_meta = {
        "ttts": "OpenAI TTS 兼容",
        "custom_voice_api": "自定义音色",
        "IndexTeam-IndexTTS-extend": "IndexTeam/IndexTTS 扩展参数"
    }
    generate_meta_json(audio_meta, target / 'api_doc' / 'audio_api' / '_meta.json')
    print(f"已生成: {target / 'api_doc' / 'audio_api' / '_meta.json'}")
    
    # best_practice 目录
    bp_meta = {
        "claudecode": "Claude Code 接入指南",
        "claudecodeccr": "Claude Code CCR",
        "codex": "OpenAI Codex 接入指南",
        "comfyui": "ComfyUI插件接入",
        "scenario": "常见客户端接入 API",
        "mcp": "MCP 说明"
    }
    generate_meta_json(bp_meta, target / 'best_practice' / '_meta.json')
    print(f"已生成: {target / 'best_practice' / '_meta.json'}")
    
    # best_practice/scenario 目录
    scenario_meta = {
        "chatbox": "Chatbox",
        "open-webui": "Open WebUI",
        "dify": "Dify",
        "cherry-studio": "Cherry-Studio",
        "claudecodekimi": "Claude Code Kimi"
    }
    generate_meta_json(scenario_meta, target / 'best_practice' / 'scenario' / '_meta.json')
    print(f"已生成: {target / 'best_practice' / 'scenario' / '_meta.json'}")
    
    # best_practice/mcp 目录
    mcp_meta = {
        "mcpgeneral": "MCP 简介",
        "MCPServer": "通过 CLINE 接入 MCP 服务",
        "MCPClient": "通过 UCloud API 实现 MCP Client"
    }
    generate_meta_json(mcp_meta, target / 'best_practice' / 'mcp' / '_meta.json')
    print(f"已生成: {target / 'best_practice' / 'mcp' / '_meta.json'}")
    
    # guide 目录
    guide_meta = {
        "briefguide": "快速入门",
        "dataset-manage": "数据集管理",
        "model-evaluation": "模型评估",
        "model-finetuning": "模型微调",
        "model-manage": "模型管理",
        "model-marketplace": "模型市场",
        "service-manage": "服务管理"
    }
    generate_meta_json(guide_meta, target / 'guide' / '_meta.json')
    print(f"已生成: {target / 'guide' / '_meta.json'}")
    
    print("\n" + "="*50)
    print(f"转换完成！输出目录：{target}")
    print("="*50)

if __name__ == '__main__':
    main()

