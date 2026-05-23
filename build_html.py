"""生成本地可用的自包含HTML看板，双击即可打开"""
import json
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(PROJECT_DIR, "data", "articles.json")
HTML_TEMPLATE = os.path.join(PROJECT_DIR, "web", "index.html")
OUTPUT_FILE = os.path.join(PROJECT_DIR, "APEC动态看板.html")


def main():
    # 读取数据
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 读取HTML模板
    with open(HTML_TEMPLATE, "r", encoding="utf-8") as f:
        html = f.read()

    # 在 </body> 前注入数据
    data_json = json.dumps(data, ensure_ascii=False)
    inject = f'<script>window.__APEC_DATA__ = {data_json};</script>'
    html = html.replace("</body>", f"{inject}\n</body>")

    # 输出
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"已生成: {OUTPUT_FILE}")
    print(f"收录 {data.get('total_articles', 0)} 篇文章")


if __name__ == "__main__":
    main()
