import os
import re
import requests

# -------------------------- 配置区 --------------------------
# 固定保存根目录
BASE_DIR = "public/libs"
# 匹配script标签中src的正则
SRC_PATTERN = re.compile(r'<script[^>]+src=["\'](.*?)["\']', re.IGNORECASE)
# 需要剔除的CDN域名前缀（自动适配主流CDN）
CDN_PREFIXES = [
    "https://cdn.jsdelivr.net/npm/",
    "https://unpkg.com/",
    "https://cdn.sheetjs.com/",
]


# -------------------------- 核心逻辑 --------------------------
def parse_scripts(script_text):
    """解析输入的script标签，提取所有src链接"""
    urls = SRC_PATTERN.findall(script_text)
    # 去重（避免重复下载）
    urls = list(filter(None, list(set(urls))))
    return urls


def get_save_path(url):
    """根据CDN链接，生成本地保存路径：public/libs/包@版本/xxx/xxx.js"""
    # 剔除CDN前缀，获取相对路径
    rel_path = url
    for prefix in CDN_PREFIXES:
        if rel_path.startswith(prefix):
            rel_path = rel_path.replace(prefix, "")
            break
    # 特殊处理 sheetjs 的 xlsx-0.20.1 → 统一为 xlsx@0.20.1
    rel_path = rel_path.replace("xlsx-", "xlsx@")
    # 拼接最终保存路径
    return os.path.join(BASE_DIR, rel_path)


def download_file(url, save_path):
    """下载单个文件并保存"""
    try:
        # 创建目录
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        # 下载
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        # 保存
        with open(save_path, "wb") as f:
            f.write(resp.content)
        print(f"✅ 下载成功：{save_path}")
        return True
    except Exception as e:
        print(f"❌ 下载失败 {url}：{str(e)}")
        return False


def generate_local_scripts(urls):
    """生成本地引用的script标签"""
    print("\n" + "=" * 60)
    print("📋 直接复制以下代码替换原CDN标签：")
    print("=" * 60)
    for url in urls:
        local_path = get_save_path(url)
        # 生成html引用路径（./开头，适配绝大多数项目）
        html_path = "./" + local_path.replace("\\", "/")
        print(f'<script src="{html_path}"></script>')


# -------------------------- 运行入口 --------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("📥 CDN资源自动下载工具 - 保存到 public/libs/")
    print("⚠️  直接粘贴所有 <script> 标签，粘贴完成后按 Ctrl+Z(Windows) / Ctrl+D(Mac) 回车")
    print("=" * 60)

    # 读取用户输入的所有script标签
    script_input = []
    while True:
        try:
            line = input()
            script_input.append(line)
        except EOFError:
            break
    script_text = "\n".join(script_input)

    # 解析+下载
    urls = parse_scripts(script_text)
    if not urls:
        print("❌ 未解析到任何script src链接")
        exit()

    print(f"\n🚀 共解析到 {len(urls)} 个JS文件，开始下载...")
    for url in urls:
        save_path = get_save_path(url)
        download_file(url, save_path)

    # 生成本地引用代码
    generate_local_scripts(urls)