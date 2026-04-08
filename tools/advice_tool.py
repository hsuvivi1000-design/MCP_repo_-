"""
Tool：取得隨機心靈雞湯

當工程師 bug 修不好時，給予一句安慰或心靈雞湯。
"""

import requests

def get_advice_data() -> str:
    """呼叫 Advice Slip API，回傳一則心靈雞湯"""
    resp = requests.get("https://api.adviceslip.com/advice", timeout=10)
    resp.raise_for_status()
    return resp.json()["slip"]["advice"]

if __name__ == "__main__":
    print(get_advice_data())
