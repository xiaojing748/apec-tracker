"""生成本地可用的自包含HTML看板"""
import json
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(PROJECT_DIR, "data", "articles.json")
HTML_FILE = os.path.join(PROJECT_DIR, "web", "index.html")
CSS_FILE = os.path.join(PROJECT_DIR, "web", "style.css")
JS_FILE = os.path.join(PROJECT_DIR, "web", "app.js")


def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    with open(CSS_FILE, "r", encoding="utf-8") as f:
        css = f.read()
    with open(JS_FILE, "r", encoding="utf-8") as f:
        js = f.read()
    with open(HTML_FILE, "r", encoding="utf-8") as f:
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

    # 输出两个版本
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


if __name__ == "__main__":
    main()
