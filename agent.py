import asyncio
import os
import json
from dotenv import load_dotenv

# 使用 google-genai 最新套件
from google import genai
from google.genai import types

from mcp import ClientSession
from mcp.client.sse import sse_client

load_dotenv()

async def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("錯誤：請在 .env 檔案中設定 GEMINI_API_KEY")
        return

    # 初始化 Gemini 客戶端
    client = genai.Client(api_key=api_key)

    print("正在連接到 MCP Server...")
    # 連接到 MCP Server
    async with sse_client("http://localhost:8000/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("MCP Server 連接成功！\n")

            # 取得所有 Tools
            tools_response = await session.list_tools()
            mcp_tools = tools_response.tools

            # 將 MCP Tools 轉換為 Gemini Function Declarations
            gemini_tools = []
            for tool in mcp_tools:
                gemini_tools.append({
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                })

            print(f"從 MCP Server 匯入了 {len(gemini_tools)} 個工具。")

            # 建立 Gemini Chat Session，並掛載工具
            chat = client.chats.create(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    tools=gemini_tools if gemini_tools else None,
                )
            )

            print("─────────────────────────────")
            print("🤖 Gemini Agent 已啟動！輸入 'quit' 或 'exit' 離開。")
            print("─────────────────────────────")

            while True:
                user_msg = input("\n你：")
                if user_msg.strip().lower() in ["quit", "exit"]:
                    break
                if not user_msg.strip():
                    continue

                try:
                    # 傳送訊息給 Gemini
                    response = chat.send_message(user_msg)
                    
                    # 檢查 Gemini 是否想要呼叫 Tool
                    while response.function_calls:
                        for fc in response.function_calls:
                            tool_name = fc.name
                            tool_args = fc.args
                            
                            print(f"\n[Debug] 🤖 Agent 正在呼叫工具：{tool_name}")
                            print(f"[Debug] 參數：{tool_args}")
                            
                            # 透過 MCP 執行 Tool
                            result = await session.call_tool(tool_name, arguments=tool_args)
                            
                            # 解析 Tool 回傳的結果
                            if result.isError:
                                tool_result_str = f"Error: {result.content}"
                            else:
                                # result.content 通常是一個 TextContent 的列表，把它轉回文字
                                tool_result_str = "\n".join(
                                    [c.text for c in result.content if hasattr(c, 'text')]
                                )
                                
                            print(f"[Debug] 工具執行完成，結果長度：{len(tool_result_str)}")
                            
                            # 把結果傳回給 Gemini
                            response = chat.send_message(
                                types.Content(
                                    parts=[
                                        types.Part.from_function_response(
                                            name=tool_name,
                                            response={"result": tool_result_str}
                                        )
                                    ]
                                )
                            )
                    
                    # Tool 呼叫完畢，或者沒有呼叫，顯示最終文字結果
                    if response.text:
                        print(f"\n🤖 Agent：\n{response.text}")

                except Exception as e:
                    print(f"\n[錯誤] 與 Gemini 溝通或執行工具時發生問題：{e}")

if __name__ == "__main__":
    asyncio.run(main())
