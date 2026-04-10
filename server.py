"""
W8 分組實作：MCP Server
主題：B：開發者工具箱
主題：開發者工具箱 MCP Server

分工說明：
- 各組員在 tools/ 建立自己的 Tool，import 到這裡用 @mcp.tool() 註冊
- 指定一位組員負責 @mcp.resource()
- 指定一位組員負責 @mcp.prompt()
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("第6組-server")


# ════════════════════════════════
#  Tools：各組員各自負責一個 Tool
# ════════════════════════════════

from tools.advice_tool import get_advice_data

from tools.joke_tool import get_joke_data


@mcp.tool()
def get_joke() -> str:
    """取得一則隨機英文笑話（Dad Joke）。
    當使用者覺得累、心情不好、或想聽笑話時使用。"""
    return get_joke_data()

@mcp.tool()
def get_advice() -> str:
    """提供心靈雞湯。
    當使用者 bug 修不好時，或者是感到挫折時使用。"""
    return get_advice_data()
from tools.cat_fact_tool import get_cat_fact_data

@mcp.tool()
def get_cat_fact() -> str:
    """休息時間冷知識：呼叫 Cat Facts API，取得隨機貓咪冷知識。"""
    return get_cat_fact_data()

from tools.web_search_tool import search_web_data

@mcp.tool()
def hello(name: str) -> str:
    """跟使用者打招呼。測試用，確認 MCP Server 正常運作。"""
    return f"你好，{name}！MCP Server 運作正常 🎉"

from tools.activity_tool import get_random_activity

@mcp.tool()
def suggest_activity() -> str:
    """取得一個隨機活動建議。
    當使用者不知道要做什麼、覺得無聊，或者想站起來做點別的事情時使用。"""
    return get_random_activity()


@mcp.tool()
def web_search(query: str) -> str:
    """搜尋網路上的技術文件與資訊。
    當使用者需要查詢最新的技術文件、程式碼解法或任何網路資訊時使用。"""
    return search_web_data(query)


# ════════════════════════════════
#  Resource：提供靜態參考資料
#  URI 格式：info://名稱 或 docs://名稱
# ════════════════════════════════

@mcp.resource("docs://shortcuts")
def get_shortcuts() -> str:
    """常用開發快捷鍵與指令速查表"""
    return (
        "VS Code 快捷鍵：\n"
        "- Ctrl+P / Cmd+P：快速開檔\n"
        "- Ctrl+Shift+P：指令面板\n"
        "- Alt+Click：多重游標\n\n"
        "Git 常用指令：\n"
        "- git status：查看狀態\n"
        "- git add . ：加入所有變更\n"
        "- git commit -m 'msg'：提交\n"
        "- git push：推送"
    )


# ════════════════════════════════
#  Prompt：整合多個 Tool 的提示詞模板
#  使用者透過 /use <名稱> [參數] 呼叫
# ════════════════════════════════

@mcp.prompt()
def debug_break() -> str:
    """當 code 除錯除到崩潰時的放鬆提示詞"""
    return (
        "我剛剛一直在除錯，需要放鬆一下。請幫我：\n"
        "1. 說一個讓我笑的笑話\n"
        "2. 給我一則激勵繼續寫 code 的人生建議\n"
        "3. 建議一個讓我起身活動 5 分鐘的活動\n"
        "請用輕鬆幽默的語氣。"
    )


if __name__ == "__main__":
    print("MCP Server 啟動中... http://localhost:8000")
    mcp.run(transport="sse")
