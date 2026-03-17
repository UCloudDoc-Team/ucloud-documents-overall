#!/usr/bin/env python3
"""
将 agent-sandbox 文档从 docsify 格式转换为 Nextra 格式
"""

import os
import re
import json
import shutil
from pathlib import Path

SOURCE_DIR = "agent-sandbox"
TARGET_DIR = "agent-sandbox_new"

def convert_links_in_content(content):
    """转换文档内容中的链接格式"""
    # 将 docs/xxx.md 或 (xxx.md) 转换为相对路径
    def replace_link(match):
        text = match.group(1)
        path = match.group(2)
        
        # 移除 .md 后缀
        path = re.sub(r'\.md$', '', path)
        
        # 处理 docs/ 前缀 - 移除它因为我们把 docs 内容提升了
        path = re.sub(r'^docs/', '/', path)
        
        # 处理 _glossary -> glossary
        path = path.replace('_glossary', '/glossary')
        
        # 处理 README -> /
        if path == 'README' or path == '/README':
            path = '/'
        
        # 确保路径以 / 开头
        if not path.startswith('/'):
            path = '/' + path
            
        return f'[{text}]({path})'
    
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, content)
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
    
    # 复制根目录文件
    # README.md -> index.md
    readme_src = source / 'README.md'
    if readme_src.exists():
        copy_and_convert_file(readme_src, target / 'index.md')
        print(f"已转换: {readme_src} -> {target / 'index.md'}")
    
    # _glossary.md -> glossary.md
    glossary_src = source / '_glossary.md'
    if glossary_src.exists():
        copy_and_convert_file(glossary_src, target / 'glossary.md')
        print(f"已转换: {glossary_src} -> {target / 'glossary.md'}")
    
    # 复制 images 目录
    images_src = source / 'images'
    if images_src.exists():
        for img_file in images_src.rglob('*'):
            if img_file.is_file():
                rel_path = img_file.relative_to(source)
                dst_file = target / rel_path
                copy_and_convert_file(img_file, dst_file)
                print(f"已复制: {img_file} -> {dst_file}")
    
    # 复制 docs 目录内容到根目录（提升一级）
    docs_src = source / 'docs'
    if docs_src.exists():
        for src_file in docs_src.rglob('*'):
            if src_file.is_file() and not src_file.name.startswith('.'):
                # 计算相对于 docs 的路径
                rel_path = src_file.relative_to(docs_src)
                dst_file = target / rel_path
                copy_and_convert_file(src_file, dst_file)
                print(f"已转换: {src_file} -> {dst_file}")
    
    # 生成 _meta.json 文件
    
    # 根目录 _meta.json
    root_meta = {
        "index": "概览",
        "cli": "UCloud Sandbox CLI",
        "sdk": "SDK 指南",
        "glossary": "词汇表"
    }
    generate_meta_json(root_meta, target / '_meta.json')
    print(f"已生成: {target / '_meta.json'}")
    
    # cli 目录 _meta.json
    cli_meta = {
        "uagentbox-cli": "UCloud Sandbox CLI"
    }
    generate_meta_json(cli_meta, target / 'cli' / '_meta.json')
    print(f"已生成: {target / 'cli' / '_meta.json'}")
    
    # sdk 目录 _meta.json
    sdk_meta = {
        "sandbox": "沙箱管理",
        "template": "模板管理",
        "commands": "命令执行",
        "filesystem": "文件系统"
    }
    generate_meta_json(sdk_meta, target / 'sdk' / '_meta.json')
    print(f"已生成: {target / 'sdk' / '_meta.json'}")
    
    # sdk/sandbox 目录 _meta.json
    sandbox_meta = {
        "01-lifecycle": "生命周期",
        "04-persistence": "数据持久化",
        "05-metrics": "指标监控",
        "06-metadata": "元数据管理",
        "07-environment-variables": "环境变量",
        "08-list": "列表查询",
        "09-connect-to-running-sanbox": "手动连接沙箱",
        "10-internet-access": "网络/互联网访问",
        "11-connect-bucket": "连接存储桶",
        "12-rate-limit": "频率限制"
    }
    generate_meta_json(sandbox_meta, target / 'sdk' / 'sandbox' / '_meta.json')
    print(f"已生成: {target / 'sdk' / 'sandbox' / '_meta.json'}")
    
    # sdk/template 目录 _meta.json
    template_meta = {
        "01-quick-start": "快速开始",
        "02-how-it-works": "工作原理",
        "03-user-and-work-dir": "用户与工作目录",
        "04-cache": "缓存机制",
        "05-base-image": "基础镜像",
        "06-private-registries": "私有仓库",
        "07-defining-template": "定义模板",
        "08-start-and-ready-commands": "启动与就绪命令",
        "09-build": "构建模板",
        "10-logging": "日志查看",
        "11-error-handling": "错误处理",
        "12-examples": "示例库"
    }
    generate_meta_json(template_meta, target / 'sdk' / 'template' / '_meta.json')
    print(f"已生成: {target / 'sdk' / 'template' / '_meta.json'}")
    
    # sdk/commands 目录 _meta.json
    commands_meta = {
        "01-overview": "概述",
        "02-streaming": "流式输出",
        "03-run-commands-in-background": "后台运行命令"
    }
    generate_meta_json(commands_meta, target / 'sdk' / 'commands' / '_meta.json')
    print(f"已生成: {target / 'sdk' / 'commands' / '_meta.json'}")
    
    # sdk/filesystem 目录 _meta.json
    filesystem_meta = {
        "01-overview": "概述",
        "02-read-and-write": "读写文件",
        "03-file-and-directory-metadata": "元数据信息",
        "04-watch-directory-for-changes": "目录监听",
        "05-upload-data": "上传数据",
        "06-download-data": "下载数据"
    }
    generate_meta_json(filesystem_meta, target / 'sdk' / 'filesystem' / '_meta.json')
    print(f"已生成: {target / 'sdk' / 'filesystem' / '_meta.json'}")
    
    print("\n" + "="*50)
    print(f"转换完成！输出目录：{target}")
    print("="*50)

if __name__ == '__main__':
    main()
