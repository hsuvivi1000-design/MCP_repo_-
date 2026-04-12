"""
Tool：搜尋技術文件 (Web Search)

使用 duckduckgo-search 來搜尋網路上的技術文件並回傳摘要結果。
"""

from duckduckgo_search import DDGS

# Tool 資訊（給人看的，不影響 MCP）
TOOL_INFO = {
    "name": "web_search",
    "api": "duckduckgo-search",
    "author": "hayashitogi",
}

def search_web_data(query: str, max_results: int = 3) -> str:
    """使用 DuckDuckGo 搜尋網路並回傳前幾個結果"""
    try:
        results = DDGS().text(query, max_results=max_results)
        if not results:
            return f"❌ 找不到與「{query}」相關的結果。"
        
        output = [f"🔍 搜尋結果：「{query}」\n"]
        for i, res in enumerate(results, 1):
            title = res.get('title', '無標題')
            href = res.get('href', '')
            body = res.get('body', '')
            output.append(f"{i}. {title}")
            output.append(f"   連結: {href}")
            output.append(f"   摘要: {body}\n")
            
        return "\n".join(output)
    except Exception as e:
        return f"⚠️ 搜尋時發生錯誤：{e}"

# 單獨測試
if __name__ == "__main__":
    print(search_web_data("Python FastAPI 教學"))
