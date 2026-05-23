"""生成本地可用的自包含HTML看板，把CSS和JS都嵌入，双击即可打开"""
import json
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(PROJECT_DIR, "data", "articles.json")
HTML_FILE = os.path.join(PROJECT_DIR, "web", "index.html")
CSS_FILE = os.path.join(PROJECT_DIR, "web", "style.css")
JS_FILE = os.path.join(PROJECT_DIR, "web", "app.js")
OUTPUT_FILE = os.path.join(PROJECT_DIR, "APEC动态看板.html")


def main():
    # 读取数据
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 读取CSS
    with open(CSS_FILE, "r", encoding="utf-8") as f:
        css = f.read()

    # 读取JS
    with open(JS_FILE, "r", encoding="utf-8") as f:
        js = f.read()

    # 读取HTML模板
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # 注入数据（在所有脚本之前）
    data_json = json.dumps(data, ensure_ascii=False)
    data_inject = "<script>window.__APEC_DATA__ = " + data_json + ";</script>"

    # 替换外部CSS引用为内联样式
    html = html.replace(
        '<link rel="stylesheet" href="style.css">',
        "<style>\n" + css + "\n</style>"
    )

    # 替换外部JS引用为内联脚本+数据注入
    html = html.replace(
        '<script src="app.js"></script>',
        data_inject + "\n<script>\n" + js + "\n</script>"
    )

    # 输出
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    total = data.get("total_articles", len(data.get("articles", [])))
    print("已生成: " + OUTPUT_FILE)
    print("收录 " + str(total) + " 篇文章")


if __name__ == "__main__":
    main()
