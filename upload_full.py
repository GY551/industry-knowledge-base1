# -*- coding: utf-8 -*-
"""
冶金矿产行业线知识库 - GitHub上传脚本（完整版）
"""
import os
import sys

def upload_to_github():
    print("=" * 50)
    print("冶金矿产行业线知识库 - GitHub上传工具")
    print("=" * 50)
    
    token = input("\n请输入GitHub Personal Access Token: ").strip()
    if not token:
        print("错误：Token不能为空")
        return
    
    username = input("请输入GitHub用户名: ").strip()
    if not username:
        print("错误：用户名不能为空")
        return
    
    repo_name = input("请输入仓库名(默认: industry-knowledge-base1): ").strip()
    if not repo_name:
        repo_name = "industry-knowledge-base1"
    
    print(f"\n正在连接GitHub...")
    
    try:
        from github import Github
        g = Github(token)
        user = g.get_user()
        print(f"已登录: {user.login}")
    except Exception as e:
        print(f"登录失败: {e}")
        return
    
    # 获取或创建仓库
    print(f"\n检查仓库 {repo_name} ...")
    try:
        repo = g.get_repo(f"{username}/{repo_name}")
        print("仓库已存在")
    except:
        print("仓库不存在，正在创建...")
        try:
            repo = user.create_repo(
                name=repo_name,
                description="冶金矿产行业线知识库",
                private=False,
                auto_init=True
            )
            print(f"仓库创建成功")
        except Exception as e:
            print(f"创建仓库失败: {e}")
            return
    
    # 上传所有文件
    base_path = r"C:\Users\BJ7070\WorkBuddy\20260324105325\industry-knowledge-base1"
    
    print(f"\n开始上传文件（包含子目录）...")
    uploaded = 0
    updated = 0
    failed = 0
    
    for root, dirs, files in os.walk(base_path):
        rel_dir = os.path.relpath(root, base_path)
        
        for f in files:
            file_path = os.path.join(root, f)
            if rel_dir == '.':
                rel_path = f
            else:
                rel_path = os.path.join(rel_dir, f).replace('\\', '/')
            
            try:
                with open(file_path, 'rb') as f_obj:
                    content = f_obj.read()
                
                # 检查文件是否已存在
                try:
                    existing = repo.get_contents(rel_path)
                    repo.update_file(
                        path=rel_path,
                        message=f"Update {rel_path}",
                        content=content,
                        sha=existing.sha
                    )
                    print(f"  更新: {rel_path}")
                    updated += 1
                except:
                    repo.create_file(
                        path=rel_path,
                        message=f"Upload {rel_path}",
                        content=content
                    )
                    print(f"  上传: {rel_path}")
                    uploaded += 1
            except Exception as e:
                print(f"  失败 {rel_path}: {e}")
                failed += 1
    
    print(f"\n✅ 完成! 新上传: {uploaded}, 更新: {updated}, 失败: {failed}")
    print(f"\n请到 https://github.com/{username}/{repo_name} 查看")
    print(f"网站地址: https://{username}.github.io/{repo_name}/")

if __name__ == "__main__":
    upload_to_github()