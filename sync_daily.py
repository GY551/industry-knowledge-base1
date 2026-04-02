"""
冶金矿产行业线知识库 - 自动同步脚本
每次生成新日报后，运行此脚本即可自动同步到知识库

用法：
    python sync_daily.py [HTML文件路径]

示例：
    python sync_daily.py "C:/Users/BJ7070/Desktop/老G日报/冶金矿产_每日资讯_20260403_商务版.html"

或不带参数，自动扫描桌面日报文件夹中的最新文件：
    python sync_daily.py
"""

import os
import re
import json
import shutil
import sys
from datetime import datetime

DESKTOP_DAILY_DIR = r"C:\Users\BJ7070\Desktop\老G日报"
KB_DAILY_DIR = r"C:\Users\BJ7070\WorkBuddy\20260324105325\industry-knowledge-base\files\daily"
KB_DATA_JS = r"C:\Users\BJ7070\WorkBuddy\20260324105325\industry-knowledge-base\assets\js\data.js"
KB_INDEX_HTML = r"C:\Users\BJ7070\WorkBuddy\20260324105325\industry-knowledge-base\index.html"


def find_new_html(specific_path=None):
    """查找需要同步的HTML文件"""
    if specific_path and os.path.exists(specific_path):
        return [specific_path]
    
    # 扫描桌面日报目录
    existing_files = set(os.listdir(KB_DAILY_DIR)) if os.path.exists(KB_DAILY_DIR) else set()
    new_files = []
    
    if os.path.exists(DESKTOP_DAILY_DIR):
        for f in os.listdir(DESKTOP_DAILY_DIR):
            if f.startswith("冶金矿产_每日资讯_") and f.endswith("_商务版.html"):
                if f not in existing_files:
                    new_files.append(os.path.join(DESKTOP_DAILY_DIR, f))
    
    return new_files


def extract_date_from_filename(filename):
    """从文件名提取日期，如 冶金矿产_每日资讯_20260403_商务版.html -> 2026-04-03"""
    m = re.search(r'(\d{8})', filename)
    if m:
        d = m.group(1)
        return f"{d[:4]}-{d[4:6]}-{d[6:8]}", d
    return None, None


def format_display_date(date_str):
    """格式化显示日期，2026-04-03 -> 2026年4月3日"""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return f"{dt.year}年{dt.month}月{dt.day}日"
    except:
        return date_str


def update_data_js(new_entries):
    """更新 data.js 文件，在 dailyNews 数组最前面插入新条目"""
    if not new_entries:
        return
    
    with open(KB_DATA_JS, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 生成新条目的JS字符串
    new_js_entries = []
    for entry in new_entries:
        js_entry = f"""    {{
      id: "daily-{entry['date'].replace('-', '')}",
      title: "冶金矿产行业线每日资讯",
      date: "{entry['date']}",
      displayDate: "{entry['displayDate']}",
      type: "html",
      file: "files/daily/{entry['filename']}",
      tags: ["每日资讯"],
      highlights: []
    }},"""
        new_js_entries.append(js_entry)
    
    # 在 dailyNews: [ 后面插入
    insert_str = "\n".join(new_js_entries) + "\n"
    content = content.replace(
        "  // 新增日报时在此数组最前面添加一条记录\n  dailyNews: [\n",
        f"  // 新增日报时在此数组最前面添加一条记录\n  dailyNews: [\n{insert_str}"
    )
    
    # 更新 lastUpdated
    today = datetime.now().strftime("%Y-%m-%d")
    content = re.sub(r'lastUpdated: "[^"]*"', f'lastUpdated: "{today}"', content)
    
    with open(KB_DATA_JS, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ data.js 已更新，新增 {len(new_entries)} 条记录")


def sync():
    """主同步流程"""
    specific = sys.argv[1] if len(sys.argv) > 1 else None
    new_files = find_new_html(specific)
    
    if not new_files:
        print("✅ 没有新文件需要同步")
        return
    
    print(f"发现 {len(new_files)} 个新文件需要同步：")
    for f in new_files:
        print(f"  · {os.path.basename(f)}")
    
    os.makedirs(KB_DAILY_DIR, exist_ok=True)
    
    new_entries = []
    for src in new_files:
        filename = os.path.basename(src)
        dst = os.path.join(KB_DAILY_DIR, filename)
        shutil.copy2(src, dst)
        print(f"  ✅ 已复制: {filename}")
        
        date_str, date_num = extract_date_from_filename(filename)
        if date_str:
            new_entries.append({
                'date': date_str,
                'displayDate': format_display_date(date_str),
                'filename': filename,
                'date_num': date_num
            })
    
    # 按日期倒序排列（最新的在前）
    new_entries.sort(key=lambda x: x['date'], reverse=True)
    
    # 更新 data.js
    update_data_js(new_entries)
    
    print("\n🎉 同步完成！知识库已更新。")
    print(f"📂 知识库路径: C:\\Users\\BJ7070\\WorkBuddy\\20260324105325\\industry-knowledge-base\\index.html")


if __name__ == '__main__':
    sync()
