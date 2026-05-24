"""生成本地可用的自包含HTML看板 + 存档页"""
import json
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(PROJECT_DIR, "data", "articles.json")


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
    """生成存档页（保持引用 archive/index.json 即可，无需自包含）"""
    src = os.path.join(PROJECT_DIR, "archive.html")
    # 存档页直接使用，无需内联——index.json 动态加载
    if os.path.exists(src):
        import shutil
        dst = os.path.join(PROJECT_DIR, "docs", "archive.html")
        shutil.copy2(src, dst)
        print("Generated: docs/archive.html")


def main():
    build_main()
    build_archive()


if __name__ == "__main__":
    main()
