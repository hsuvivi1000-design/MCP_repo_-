# MCP Server + AI agent 分組實作

> 課程：AI Agent 開發 — MCP（Model Context Protocol）
> 主題：開發者工具箱 MCP Server

---

## Server 功能總覽

> 說明這個 MCP Server 提供哪些 Tool

| Tool 名稱                 | 功能說明     | 負責組員 |
| ------------------------- | ------------ | -------- |
| `web_search_tool` | 搜尋技術文件 |  林伽紜        |
|  `get_joke`     |   獲得隨機冷笑話 | 朱覺祥  |
| `activity_tool` | 獲得隨機活動建議 | 林湘紜 |
| `get_cat_fact_data`       | 休息時間冷知識 |     姚谷伝     |
|`get_advice_tool`| bug 修不好時的心靈雞湯|    許瀞云      |

---

## 組員與分工

| 姓名 | 負責功能            | 檔案          | 使用的 API |
| ---- | ------------------- | ------------- | ---------- |
| 林伽紜     |  搜尋技術文件   | `tools/web_search_tool.py`    | duckduckgo-search |
| 許瀞云| bug 修不好時的心靈雞湯 | `tools/advice_tool.py`    |            |
| 朱覺祥 |  get_joke Tool   | `tools/joke_tool.py`    | icanhazdadjoke  |
|姚谷伝 | 休息時間冷知識| `tools/cat_fact_tool.py`|  https://catfact.ninja/fact      |
|林湘紜 | 獲得隨機活動建議| `tools/activity_tool.py`|  bored-api  |
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
│   ├── web_search_tool.py        # 林伽紜 的 Tool
│   ├── tools/advice_tool.py        # 朱覺祥 的 Tool
│   └── activity_tool.py        # 林湘紜 的 Tool
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
<img width="1917" height="866" alt="螢幕擷取畫面 2026-04-10 132246" src="https://github.com/user-attachments/assets/a64c61a7-e4b8-4f6b-85e3-b5526a38707c" />
<img width="1919" height="860" alt="螢幕擷取畫面 2026-04-10 132326" src="https://github.com/user-attachments/assets/7bd1e800-cd3b-404e-a4f6-4bac9685b75e" />
<img width="1919" height="867" alt="螢幕擷取畫面 2026-04-10 132405" src="https://github.com/user-attachments/assets/e5dc6ff9-1de7-484d-a944-03b63278a0b6" />


### Agent 對話截圖

> 貼上 Agent 對話的截圖（顯示 Gemini 呼叫 Tool 的過程，以及使用 /use 呼叫 Prompt 的結果）
<img width="952" height="374" alt="螢幕擷取畫面 2026-04-10 133314" src="https://github.com/user-attachments/assets/c0e4f708-3307-4fbb-b04f-d2b2fe631a35" />
<img width="950" height="530" alt="螢幕擷取畫面 2026-04-10 133625" src="https://github.com/user-attachments/assets/bee44160-1632-4932-b9d5-327e0845ecb2" />

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

### `get_advice_tool`（負責：許瀞云）

- **功能**：bug 修不好時的心靈雞湯
- **使用 API**：https://api.adviceslip.com/advice
- **參數**：
- **回傳範例**： `"Today, do not use the words "Kind of", "Sort of" or "Maybe". It either is or it isn't."`


### `get_joke`（負責：朱覺祥）
**功能**：取得一則隨機英文笑話（Dad Joke），當使用者覺得累、心情不好時使用。
- **使用 API**：`https://icanhazdadjoke.com/`
- **參數**：無
- **回傳範例**：`"Why couldn't the kid see the pirate movie? Because it was rated arrr!"`

```python
@mcp.tool()
def get_joke() -> str:
    """取得一則隨機英文笑話（Dad Joke）。
    當使用者覺得累、心情不好、或想聽笑話時使用。"""
    return get_joke_data()
```

### `activity_tool`（負責：林湘紜）
**功能**：獲得隨機活動建議。
- **使用 API**：`https://bored-api.appbrewery.com/random`
- **參數**：無
- **回傳範例**：`建議活動：Learn about a distributed version control system such as Git
活動類型：education`

```python
@mcp.tool()
def suggest_activity() -> str:
    """取得一個隨機活動建議。
    當使用者不知道要做什麼、覺得無聊，或者想站起來做點別的事情時使用。"""
    return get_random_activity()
```

---

## 心得

### 遇到最難的問題

> 遇到了外部 API 服務無預警掛掉與套件改版的問題。原本想串接的 numbersapi.com 剛好全球伺服器故障（全面回傳 404 Not Found），後來改為實作 duckduckgo-search 來獲取技術文件時，又遇到該套件剛發生重大更新，把內部模組名稱統一是 ddgs，導致原本的官方範例程式碼無法運作、默默回傳空陣列。解決方式： 透過終端機進行 Debug 測試找到報錯原因，將套件名稱與 Import 語法更新為最新的 from ddgs import DDGS，讓程式成功運作！

### MCP 跟上週的 Tool Calling 有什麼不同？

> 把伺服器跟客戶端分開。我們可以把各種資料庫查詢、API 搜尋（像 DuckDuckGo）封裝成一個獨立的工具箱，不僅容易維護，安全性也更好。
