"""生成本地可用的自包含HTML看板 + 存档页"""
import json
import os
import shutil

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(PROJECT_DIR, "data", "articles.json")
ARCHIVE_INDEX = os.path.join(PROJECT_DIR, "archive", "index.json")


def build_main():
    """生成主看板自包含版"""
    web_dir = os.path.join(PROJECT_DIR, "web")
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    with open(os.path.join(web_dir, "style.css"), "r", encoding="utf-8") as f:
        css = f.read()
    with open(os.path.join(web_dir, "app.js"), "r", encoding="utf-8") as f:
        js = f.read()
    with open(os.path.join(web_dir, "index.html"), "r", encoding="utf-8") as f:
        html = f.read()

    data_json = json.dumps(data, ensure_ascii=False)
    data_inject = "<script>window.__APEC_DATA__ = " + data_json + ";</script>"

    html = html.replace(
        '<link rel="stylesheet" href="style.css">',
        "<style>\n" + css + "\n</style>"
    )
    html = html.replace(
        '<script src="app.js"></script>',
        data_inject + "\n<script>\n" + js + "\n</script>"
    )

    outputs = [
        os.path.join(PROJECT_DIR, "APEC动态看板.html"),
        os.path.join(PROJECT_DIR, "index.html"),
    ]
    for path in outputs:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print("Generated: " + os.path.basename(path))

    total = data.get("total_articles", len(data.get("articles", [])))
    print("Total: " + str(total) + " articles")


def build_archive():
    """生成自包含存档页——嵌入索引数据"""
    src = os.path.join(PROJECT_DIR, "archive.html")

    if not os.path.exists(src):
        print("archive.html not found, skipping")
        return

    with open(src, "r", encoding="utf-8") as f:
        html = f.read()

    # 嵌入存档索引数据
    if os.path.exists(ARCHIVE_INDEX):
        with open(ARCHIVE_INDEX, "r", encoding="utf-8") as f:
            idx_data = json.load(f)
        idx_json = json.dumps(idx_data, ensure_ascii=False)
        idx_inject = "<script>window.__ARCHIVE_DATA__ = " + idx_json + ";</script>"
    else:
        idx_inject = "<script>window.__ARCHIVE_DATA__ = {entries:[],total:0,updated:''};</script>"

    html = html.replace(
        '<script>',
        idx_inject + "\n<script>"
    )

    outputs = [
        os.path.join(PROJECT_DIR, "archive_self.html"),
        os.path.join(PROJECT_DIR, "docs", "archive.html"),
    ]
    for path in outputs:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print("Generated: " + os.path.basename(os.path.dirname(path)) + "/" + os.path.basename(path))

    # 同时复制原始archive.html到根目录（用于非自包含模式）
    shutil.copy2(src, os.path.join(PROJECT_DIR, "archive_root.html"))


def main():
    build_main()
    build_archive()


if __name__ == "__main__":
    main()
