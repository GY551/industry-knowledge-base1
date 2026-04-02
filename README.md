# 冶金矿产行业线知识库

## 快速使用

直接双击 `index.html` 即可在浏览器中打开使用。

---

## 目录结构

```
industry-knowledge-base/
├── index.html              ← 主入口，双击打开
├── assets/
│   └── js/
│       └── data.js         ← 数据配置文件（新增资料在此维护）
├── files/
│   ├── meetings/           ← 合伙人经理会议 PDF
│   ├── minutes/            ← 经营例会纪要 PNG/PPTX
│   ├── daily/              ← 每日资讯 HTML
│   ├── notices/            ← 重点通知附件（如有）
│   └── pptx-slides/        ← PPTX转换的图片组
├── sync_daily.py           ← 自动同步日报脚本
├── convert_pptx.py         ← PPTX转图片脚本
└── README.md               ← 本说明文件
```

---

## 如何新增内容

### 方法一：新增每日资讯（推荐用自动脚本）

每次生成新日报后，运行：
```
python sync_daily.py
```
脚本会自动扫描桌面`老G日报`文件夹，将新HTML文件复制到知识库并更新目录。

或手动指定文件：
```
python sync_daily.py "C:\...\冶金矿产_每日资讯_20260403_商务版.html"
```

### 方法二：手动添加（任何类型）

编辑 `assets/js/data.js` 文件，在对应数组中添加一条记录即可。

**添加 PDF 会议材料**：
```js
meetings: [
  {
    id: "meeting-20260402",
    title: "【冶金矿产行业线】第二次合伙人经理会议材料",
    date: "2026-04-02",
    version: "V20260402",
    type: "pdf",
    file: "files/meetings/文件名.pdf",
    tags: ["合伙人会议"],
    summary: "本次会议讨论要点..."
  },
  ...
]
```

**添加重点通知**：
```js
notices: [
  {
    id: "notice-001",
    title: "关于加强XXX管理的通知",
    date: "2026-04-02",
    content: "通知正文内容...",
    tag: "重要",
    tagColor: "#e53935"
  }
]
```

**添加经营例会纪要（图片格式）**：
```js
minutes: [
  {
    id: "minutes-20260501",
    title: "2026年5月1日 审计板块行业线经营例会纪要",
    date: "2026-05-01",
    type: "image",
    file: "files/minutes/2026年5月1日 审计板块行业线经营例会纪要.png",
    tags: ["经营例会", "2026年"],
    summary: "..."
  }
]
```

---

## 新增PPTX材料处理

1. 将PPTX文件复制到 `files/minutes/`
2. 编辑 `convert_pptx.py`，修改 `pptx_path` 和 `output_dir`
3. 运行 `python convert_pptx.py`
4. 在 `data.js` 的 `minutes` 数组中添加记录（type 为 `"pptx-slides"`）

---

## GitHub Pages部署（分享给同事）

1. 在GitHub新建仓库 `industry-knowledge-base`
2. 将本文件夹所有内容上传
3. 进入仓库设置 → Pages → Source选择 `main` 分支根目录
4. 等待1-2分钟，访问 `https://你的用户名.github.io/industry-knowledge-base/`
5. 将链接分享给同事即可

---

*最后更新：2026-04-02*
