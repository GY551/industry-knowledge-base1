# -*- coding: utf-8 -*-
"""
冶金矿产行业线知识库 - GitHub上传脚本
使用说明：
1. 登录GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 点击 "Generate new token" → 勾选 "repo" 权限 → 生成token
3. 运行本脚本，输入token和用户名即可自动上传
"""
import os
import sys
from github import Github

def main():
    print("=" * 50)
    print("冶金矿产行业线知识库 - GitHub上传工具")
    print("=" * 50)
    
    # 获取GitHub Token
    token = input("\n请输入GitHub Personal Access Token: ").strip()
    if not token:
        print("错误：Token不能为空")
        sys.exit(1)
    
    # 获取用户名
    username = input("请输入GitHub用户名: ").strip()
    if not username:
        print("错误：用户名不能为空")
        sys.exit(1)
    
    # 获取仓库名
    repo_name = input("请输入仓库名(默认: industry-knowledge-base): ").strip()
    if not repo_name:
        repo_name = "industry-knowledge-base"
    
    print(f"\n正在连接GitHub...")
    g = Github(token)
    
    try:
        # 获取用户
        user = g.get_user()
        print(f"已登录: {user.login}")
    except Exception as e:
        print(f"登录失败: {e}")
        sys.exit(1)
    
    # 检查仓库是否已存在
    print(f"\n检查仓库 {repo_name} ...")
    try:
        repo = g.get_repo(f"{username}/{repo_name}")
        print("仓库已存在，将上传文件到现有仓库")
    except:
        print("仓库不存在，正在创建...")
        repo = user.create_repo(
            name=repo_name,
            description="冶金矿产行业线知识库 - 会议资料、会议纪要、每日资讯",
            private=False,
            auto_init=True
        )
        print(f"仓库创建成功: https://github.com/{username}/{repo_name}")
    
    # 上传文件
    base_path = r"C:\Users\BJ7070\WorkBuddy\20260324105325\industry-knowledge-base"
    
    print(f"\n开始上传文件...")
    uploaded = 0
    failed = 0
    
    for root, dirs, files in os.walk(base_path):
        # 跳过根目录本身
        if root == base_path:
            for f in files:
                file_path = os.path.join(root, f)
                try:
                    with open(file_path, 'rb') as f_obj:
                        content = f_obj.read()
                    
                    repo.create_file(
                        path=f,
                        message=f"Upload {f}",
                        content=content
                    )
                    print(f"  上传: {f}")
                    uploaded += 1
                except Exception as e:
                    print(f"  上传失败 {f}: {e}")
                    failed += 1
            continue
        
        # 处理子目录
        rel_dir = os.path.relpath(root, base_path)
        
        for f in files:
            file_path = os.path.join(root, f)
            rel_path = os.path.join(rel_dir, f).replace('\\', '/')
            
            try:
                with open(file_path, 'rb') as f_obj:
                    content = f_obj.read()
                
                repo.create_file(
                    path=rel_path,
                    message=f"Upload {rel_path}",
                    content=content
                )
                print(f"  上传: {rel_path}")
                uploaded += 1
            except Exception as e:
                # 可能是文件已存在，尝试更新
                try:
                    existing = repo.get_contents(rel_path)
                    repo.update_file(
                        path=rel_path,
                        message=f"Update {rel_path}",
                        content=content,
                        sha=existing.sha
                    )
                    print(f"  更新: {rel_path}")
                    uploaded += 1
                except Exception as e2:
                    print(f"  上传失败 {rel_path}: {e2}")
                    failed += 1
    
    print(f"\n上传完成! 成功: {uploaded}, 失败: {failed}")
    print(f"\n请到 https://github.com/{username}/{repo_name} 查看")
    print(f"然后进入 Settings → Pages 开启 Pages 部署")

if __name__ == "__main__":
    main()