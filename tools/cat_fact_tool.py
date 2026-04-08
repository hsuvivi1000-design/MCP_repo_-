import requests

def get_cat_fact_data() -> str:
    """呼叫 Cat Facts API，回傳一則貓咪冷知識"""
    try:
        resp = requests.get("https://catfact.ninja/fact", timeout=10)
        resp.raise_for_status()
        return resp.json().get("fact", "找不到貓咪冷知識")
    except Exception as e:
        return f"取得貓咪冷知識時發生錯誤：{str(e)}"
