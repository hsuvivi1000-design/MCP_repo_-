# MCP Server + AI agent 分組實作

> 課程：AI Agent 開發 — MCP（Model Context Protocol）
> 主題：（填入你們選的主題）

---

## Server 功能總覽

> 說明這個 MCP Server 提供哪些 Tool

| Tool 名稱                 | 功能說明     | 負責組員 |
| ------------------------- | ------------ | -------- |
| （範例：`get_weather`） | 查詢即時天氣 |          |
| `get_cat_fact_data`       | 休息時間冷知識 |     姚谷伝     |
|                           |              |          |

---

## 組員與分工

| 姓名 | 負責功能            | 檔案          | 使用的 API |
| ---- | ------------------- | ------------- | ---------- |
|      |                     | `tools/`    |            |
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
│   ├── cat_fact_tool.py   # 姚谷伝 的 Tool
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

### `get_cat_fact`（負責：姚谷伝）

- **功能**：呼叫 Cat Facts API，取得一則隨機的貓咪冷知識，供休息時間娛樂使用。
- **使用 API**：`https://catfact.ninja/fact`
- **參數**：無（不需傳遞參數）
- **回傳範例**：`"Cats are the most popular pet in the United States: There are 88 million pet cats and 74 million dogs."`

```python
@mcp.tool()
def get_cat_fact() -> str:
    """休息時間冷知識：呼叫 Cat Facts API，取得隨機貓咪冷知識。"""
    ...
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

最困難的是在將自己的 Tool 合併至 `server.py` 的時候，需要確保每個組員的 import 路徑和 function 命名都是獨立的（以免在合併 commit 時互相衝突）。
解決方式：透過制定明確的分支開發流程（Git Feature Branch `feature/cat-fact`），並統一將邏輯保留在 `/tools` 目錄下各自專屬的檔案中，再於 `server.py` 共用註冊。

### MCP 跟上週的 Tool Calling 有什麼不同？

1. **低耦合、模組化更高**：MCP 將工具打包成獨立的伺服器（Server），不再需要將每個工具的實作細節和套件相依性硬塞在主程式裡。
2. **擴充更容易**：只要透過統一的協定連接 Server，AI Agent 可以隨時跨本地或網頁端動態地發現新工具（Tools, Resources, Prompts），省去繁瑣的硬整合操作。
3. **可重複利用性極佳**：寫好一個 MCP Server 之後，其他不同的 AI 專案或應用都能直接橋接使用，跨專案的復用性非常高！
