# MCP Server + AI agent 分組實作

> 課程：AI Agent 開發 — MCP（Model Context Protocol）
> 主題：（填入你們選的主題）

---

## Server 功能總覽

> 說明這個 MCP Server 提供哪些 Tool

| Tool 名稱                 | 功能說明     | 負責組員 |
| ------------------------- | ------------ | -------- |
| web_search | 搜尋技術文件 |  林伽紜        |
|                           |              |          |
|                           |              |          |

---

## 組員與分工

| 姓名 | 負責功能            | 檔案          | 使用的 API |
| ---- | ------------------- | ------------- | ---------- |
| 林伽紜     |  搜尋技術文件   | `tools/web_search_tool.py`    | duckduckgo-search |
|      |                     | `tools/`    |            |
|姚谷伝 | 休息時間冷知識| `tools/cat_fact_tool.py`|  https://catfact.ninja/fact      |
|      | Resource + Prompt   | `server.py` | —         |
|      | Agent（用 AI 產生） | `agent.py`  | Gemini API |

---

## 專案架構

```
├── server.py              # MCP Server 主程式
├── agent.py               # MCP Client + Gemini Agent（用 AI 產生）
├── tools/
│   ├── __init__.py
│   ├── example_tool.py    # 範例（可刪除）
│   ├── web_search_tool.py        # 組員 A 的 Tool
│   ├── xxx_tool.py        # 組員 B 的 Tool
│   └── xxx_tool.py        # 組員 C 的 Tool
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 使用方式

```bash
# 1. 建立虛擬環境
python3 -m venv .venv
source .venv/bin/activate

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 設定 API Key
cp .env.example .env
# 編輯 .env，填入你的 GEMINI_API_KEY

# 4. 用 MCP Inspector 測試 Server
mcp dev server.py

# 5. 用 Agent 對話
python agent.py
```

---

## 測試結果

### MCP Inspector 截圖

> 貼上 Inspector 的截圖（Tools / Resources / Prompts 三個分頁都要有）

### Agent 對話截圖

> 貼上 Agent 對話的截圖（顯示 Gemini 呼叫 Tool 的過程，以及使用 /use 呼叫 Prompt 的結果）

---

## 各 Tool 說明

### `web_search_tool`（負責：林伽紜）

- **功能**：搜尋技術文件
- **使用 API**：duckduckgo-search
- **參數**：
- **回傳範例**：
🔍 搜尋結果：「Python FastAPI」

1. FastAPI
   連結: https://fastapi.tiangolo.com/
   摘要: If anyone is looking to build a productionPythonAPI, I would highly recommendFastAPI. ...FastAPIapplications running under Uvicorn as one of the ...

2. Python Types Intro - FastAPI
   連結: https://fastapi.tiangolo.com/python-types/
   摘要: The important thing is that by using standardPythontypes, in a single place (instead of adding more classes, decorators, etc),FastAPIwill do a ...

3. multithreading - FastAPI python: How to run a thread in the
   連結: https://stackoverflow.com/questions/70872276/fastapi-python-how-to-run-a-thread-in-the-background
   摘要: I'm making a server inpythonusingFastAPI, and I want a function that is not related to my API, to run in the background every 5 minutes (like ...

```python
@mcp.tool()
def web_search(query: str) -> str:
    """搜尋網路上的技術文件與資訊。
    當使用者需要查詢最新的技術文件、程式碼解法或任何網路資訊時使用。"""
    return search_web_data(query)
```

### `tool_name`（負責：姓名）

- **功能**：
- **使用 API**：
- **參數**：
- **回傳範例**：

### `tool_name`（負責：姓名）

- **功能**：
- **使用 API**：
- **參數**：
- **回傳範例**：

---

## 心得

### 遇到最難的問題

> 遇到了外部 API 服務無預警掛掉與套件改版的問題。原本想串接的 numbersapi.com 剛好全球伺服器故障（全面回傳 404 Not Found），後來改為實作 duckduckgo-search 來獲取技術文件時，又遇到該套件剛發生重大更新，把內部模組名稱統一是 ddgs，導致原本的官方範例程式碼無法運作、默默回傳空陣列。解決方式： 透過終端機進行 Debug 測試找到報錯原因，將套件名稱與 Import 語法更新為最新的 from ddgs import DDGS，讓程式成功運作！

### MCP 跟上週的 Tool Calling 有什麼不同？

> 把伺服器跟客戶端分開。我們可以把各種資料庫查詢、API 搜尋（像 DuckDuckGo）封裝成一個獨立的工具箱，不僅容易維護，安全性也更好。
