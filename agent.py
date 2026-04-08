import os
import asyncio
from dotenv import load_dotenv

from google import genai
from google.genai import types

from mcp import ClientSession
from mcp.client.sse import sse_client

# 載入環境變數
load_dotenv()

async def run_agent():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "你的_Gemini_API_Key":
        print("❌ 未設定 GEMINI_API_KEY，請在 .env 檔案中填寫你的 Gemini API Key！")
        return

    # 初始化 Gemini 客戶端
    client = genai.Client(api_key=api_key)

    print("🔄 正在連接到 MCP Server (http://localhost:8000/sse)...")
    try:
        # 1. 連接到 MCP Server
        async with sse_client("http://localhost:8000/sse") as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                print("✅ 成功連接到 MCP Server!")

                # 2. 取得所有工具
                tools_response = await session.list_tools()
                available_tools = {tool.name: tool for tool in tools_response.tools}
                print(f"🔧 伺服器提供以下工具: {list(available_tools.keys())}")

                # 3. 轉換成 Gemini API 的 function declaration 格式
                gemini_tools = []
                for name, mcp_tool in available_tools.items():
                    func_decl = {
                        "name": mcp_tool.name,
                        "description": mcp_tool.description or "",
                    }
                    
                    if mcp_tool.inputSchema:
                        properties = mcp_tool.inputSchema.get("properties", {})
                        required = mcp_tool.inputSchema.get("required", [])
                        # 簡單的映射以符合 Gemini 規範
                        schema = {
                            "type": "OBJECT",
                            "properties": {
                                k: {"type": v.get("type", "STRING").upper()} 
                                for k, v in properties.items()
                            }
                        }
                        if required:
                            schema["required"] = required
                        func_decl["parameters"] = schema

                    gemini_tools.append(func_decl)

                tools_config = None
                if gemini_tools:
                    tools_config = [{"function_declarations": gemini_tools}]

                # 4. 開始多輪對話
                print("\n🤖 Gemini 2.5 Flash-Lite Agent 啟動！")
                print("💡 現在你可以跟 AI 對話了，AI 會自動評估是否呼叫對應的 Tool 來幫助你。（輸入 'quit' 退出）")
                print("-" * 50)
                
                chat = client.chats.create(model="gemini-2.5-flash-lite")
                
                while True:
                    user_input = input("你: ")
                    if user_input.lower() in ["quit", "exit"]:
                        print("👋 再見！")
                        break

                    response = chat.send_message(user_input, config=types.GenerateContentConfig(tools=tools_config))
                    
                    # 處理 possible function calls
                    while True:
                        has_function_call = False
                        
                        if response.candidates and response.candidates[0].content.parts:
                            for part in response.candidates[0].content.parts:
                                if part.function_call:
                                    has_function_call = True
                                    fn_call = part.function_call
                                    # 轉換 args 屬性（因為 Gemini 回傳可能是不同結構）
                                    # args 若有，轉換為 dict 傳給 MCP
                                    call_args = {k: v for k, v in fn_call.args.items()} if fn_call.args else {}
                                    
                                    print(f"\n  [Debug] 🛠️ Agent 決定呼叫工具: {fn_call.name}，參數: {call_args}")
                                    
                                    # 5. 透過 MCP call_tool 呼叫對應的 Tool
                                    try:
                                        tool_result = await session.call_tool(
                                            fn_call.name, 
                                            arguments=call_args
                                        )
                                        # 解析 MCP 的 Content (如果有)
                                        # 大多時候是 text 類型的結構
                                        text_result = ""
                                        for content in tool_result.content:
                                            # mcp tool 回傳可能是 dict 或對象
                                            if hasattr(content, 'type') and content.type == "text":
                                                text_result += content.text + "\n"
                                            elif hasattr(content, 'text'):
                                                text_result += content.text + "\n"
                                            else:
                                                text_result += str(content) + "\n"
                                                
                                        print(f"  [Debug] 📥 工具執行結果: {text_result.strip()}")
                                        
                                        # 把結果送回 Gemini 繼續對話
                                        response = chat.send_message(
                                            types.Part.from_function_response(
                                                name=fn_call.name,
                                                response={"result": text_result}
                                            ),
                                            config=types.GenerateContentConfig(tools=tools_config)
                                        )
                                    except Exception as e:
                                        print(f"  [Error] ❌ 執行工具失敗: {e}")
                                        response = chat.send_message(
                                            types.Part.from_function_response(
                                                name=fn_call.name,
                                                response={"error": str(e)}
                                            ),
                                            config=types.GenerateContentConfig(tools=tools_config)
                                        )
                        
                        if not has_function_call:
                            break # 如果沒有更多 function call 則結束此輪回圈

                    # 6. 直接顯示文字結果給使用者
                    print(f"AI: {response.text}\n")

    except Exception as e:
        print(f"❌ 無法連接到 Server，請確認已經先執行了 `python server.py`！\n錯誤詳細資料: {e}")

if __name__ == "__main__":
    # Windows 環境如果有 proactor 問題，可加上此行確保 asyncio 關閉順利
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(run_agent())
