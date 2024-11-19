from pixivpy3 import *
import os
import json
import requests

# 替换为你的 API 令牌
EAGLE_API_TOKEN = "YOUR_EAGLE_API_TOKEN"

# 获取access_token 和 refresh_token
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
REFRESH_TOKEN = "YOUR_REFRESH_TOKEN"


def load_tokens_from_file(file_path):
    """
    从 JSON 文件加载 Token。
    :param file_path: JSON 文件路径
    :return: 包含 token 的字典
    """
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                tokens = json.load(file)
                return tokens
        except json.JSONDecodeError:
            print(f"文件 {file_path} 格式错误，请检查。")
    return {}


def save_tokens_to_file(file_path, tokens):
    """
    将 Token 保存到 JSON 文件。
    :param file_path: JSON 文件路径
    :param tokens: 包含 token 的字典
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(tokens, file, ensure_ascii=False, indent=4)


def get_token(prompt):
    """
    询问用户输入 Token。
    :param prompt: 输入提示信息
    :return: 用户输入的 Token
    """
    token = input(prompt)
    return token.strip()


# 通过 Eagle API 保存一张图片到 eagle
def GetOnePictureToEagle(api_token, illust_id):
    json_result = api.illust_detail(illust_id)
    illust = json_result.illust
    resultTags = [item["name"] for item in illust.tags]
    link = f"https://www.pixiv.net/artworks/{illust_id}"
    url = f"http://localhost:41595/api/item/addFromURL?token={api_token}"
    data = {
        "url": illust.meta_single_page.original_image_url,
        "name": illust.title,
        "website": link,
        "tags": resultTags,
        "token": "{api_token}",
        "headers": {"referer": "www.pixiv.net"},
    }
    headers = {"Content-Type": "application/json"}
    try:
        # 发送 POST 请求
        response = requests.post(url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success":
                print("请求成功，请转到 Eagle 中查看")
            else:
                print(f"API 请求失败: {data.get('error', '未知错误')}")
        else:
            print(f"HTTP 请求失败，状态码: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        


if __name__ == "__main__":

    token_file = "tokens.json"

    # 从文件加载 Token
    tokens = load_tokens_from_file(token_file)

    # 获取 EAGLE_API_TOKEN
    EAGLE_API_TOKEN = tokens.get("EAGLE_API_TOKEN")
    if not EAGLE_API_TOKEN:
        EAGLE_API_TOKEN = get_token("请输入 EAGLE_API_TOKEN: ")
        tokens["EAGLE_API_TOKEN"] = EAGLE_API_TOKEN

    # 获取 ACCESS_TOKEN
    ACCESS_TOKEN = tokens.get("ACCESS_TOKEN")
    if not ACCESS_TOKEN:
        ACCESS_TOKEN = get_token("请输入 ACCESS_TOKEN: ")
        tokens["ACCESS_TOKEN"] = ACCESS_TOKEN

    # 获取 REFRESH_TOKEN
    REFRESH_TOKEN = tokens.get("REFRESH_TOKEN")
    if not REFRESH_TOKEN:
        REFRESH_TOKEN = get_token("请输入 REFRESH_TOKEN: ")
        tokens["REFRESH_TOKEN"] = REFRESH_TOKEN

    # 保存更新后的 Token 到文件
    save_tokens_to_file(token_file, tokens)
    # 初始化 Pixiv API
    api = AppPixivAPI()
    api.set_auth(ACCESS_TOKEN, REFRESH_TOKEN)

    picture_id = int(input("请输入作品 ID（数字）："))
    GetOnePictureToEagle(EAGLE_API_TOKEN, picture_id)
