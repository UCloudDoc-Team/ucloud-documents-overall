#!/usr/bin/env python3
"""
更新 modelverse_new 目录中的图片地址
将相对路径转换为 CDN 绝对路径
"""

import os
import re
from pathlib import Path

TARGET_DIR = "modelverse_new"
CDN_BASE = "https://static.ucloud.cn/docs/modelverse"

def update_image_urls(content):
    """更新图片地址"""
    
    # 匹配 markdown 图片语法 ![alt](url)
    # 将 /images/... 或 images/... 替换为 CDN 地址
    # 排除已经是 https:// 开头的
    
    def replace_image_url(match):
        alt = match.group(1)
        url = match.group(2)
        
        # 如果已经是 https 开头，不修改
        if url.startswith('https://') or url.startswith('http://'):
            return match.group(0)
        
        # 处理 /images/... 或 images/... 格式
        if url.startswith('/images/'):
            new_url = f"{CDN_BASE}{url}"
        elif url.startswith('images/'):
            new_url = f"{CDN_BASE}/{url}"
        elif '/images/' in url:
            # 处理 ../images/ 这种相对路径
            idx = url.find('images/')
            new_url = f"{CDN_BASE}/{url[idx:]}"
        else:
            # 其他情况不修改
            return match.group(0)
        
        return f"![{alt}]({new_url})"
    
    # 匹配 ![alt](url) 格式
    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_image_url, content)
    
    # 也处理 HTML img 标签
    def replace_img_src(match):
        before = match.group(1)
        url = match.group(2)
        after = match.group(3)
        
        if url.startswith('https://') or url.startswith('http://'):
            return match.group(0)
        
        if url.startswith('/images/'):
            new_url = f"{CDN_BASE}{url}"
        elif url.startswith('images/'):
            new_url = f"{CDN_BASE}/{url}"
        elif '/images/' in url:
            idx = url.find('images/')
            new_url = f"{CDN_BASE}/{url[idx:]}"
        else:
            return match.group(0)
        
        return f'{before}{new_url}{after}'
    
    # 匹配 <img src="..."> 格式
    content = re.sub(r'(<img[^>]*src=["\'])([^"\']+)(["\'][^>]*>)', replace_img_src, content)
    
    return content

def process_file(filepath):
    """处理单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = update_image_urls(content)
    
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    target = Path(TARGET_DIR)
    updated_count = 0
    
    for md_file in target.rglob('*.md'):
        if process_file(md_file):
            print(f"已更新: {md_file}")
            updated_count += 1
    
    print(f"\n共更新 {updated_count} 个文件")

if __name__ == '__main__':
    main()

