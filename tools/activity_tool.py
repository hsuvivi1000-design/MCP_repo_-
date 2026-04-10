import requests

def get_random_activity() -> str:
    """取得一個隨機活動建議。
    當使用者不知道要做什麼、覺得無聊，或者想站起來做點別的事情時使用。"""
    try:
        response = requests.get("https://bored-api.appbrewery.com/random")
        if response.status_code == 200:
            data = response.json()
            activity = data.get("activity", "未知活動")
            type_ = data.get("type", "未知類型")
            return f"建議活動：{activity}\n活動類型：{type_}"
        else:
            return f"目前無法取得隨機活動建議，API 回傳狀態碼：{response.status_code}"
    except Exception as e:
        return f"發生錯誤：{str(e)}"
