"""
Tool：取得隨機笑話（Dad Joke）

使用 icanhazdadjoke API，回傳一則隨機英文笑話。
適合在寫 code 寫到累的時候使用，讓你放鬆一下。
"""

import requests

# Tool 資訊
TOOL_INFO = {
    "name": "get_joke",
    "api": "https://icanhazdadjoke.com/",
    "author": "組員",
}


def get_joke_data() -> str:
    """呼叫 icanhazdadjoke API，回傳一則隨機笑話"""
    resp = requests.get(
        "https://icanhazdadjoke.com/",
        headers={"Accept": "application/json"},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["joke"]


# 單獨測試
if __name__ == "__main__":
    print(get_joke_data())
