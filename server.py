"""
W8 分組實作：MCP Server
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

# 範例（替換成符合你們主題的內容）：
#
# @mcp.resource("info://tips")
# def get_tips() -> str:
#     """（主題）的實用小提示"""
#     return (
#         "實用小提示：\n"
#         "- 提示 1\n"
#         "- 提示 2\n"
#         "- 提示 3"
#     )


# ════════════════════════════════
#  Prompt：整合多個 Tool 的提示詞模板
#  使用者透過 /use <名稱> [參數] 呼叫
# ════════════════════════════════

# 範例（替換成符合你們主題的內容）：
#
# @mcp.prompt()
# def my_plan(topic: str) -> str:
#     """產生（主題）計畫的提示詞"""
#     return (
#         f"請幫我規劃關於 {topic} 的計畫：\n"
#         f"1. 先使用相關工具取得資訊\n"
#         f"2. 根據資訊提供 3 個具體建議\n"
#         f"3. 附上一則笑話或建議讓我開心\n"
#         f"請用繁體中文回答。"
#     )


if __name__ == "__main__":
    print("MCP Server 啟動中... http://localhost:8000")
    mcp.run(transport="sse")
