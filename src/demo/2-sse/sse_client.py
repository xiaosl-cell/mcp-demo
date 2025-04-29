import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client


async def async_sse_client(name: str):
    url = "http://localhost:9000/sse"
    params = {"name": name}

    try:
        async with sse_client(url) as streams:
            async with ClientSession(*streams) as session:
                await session.initialize()

                # 获取流式响应
                call_tool_result = await session.call_tool("hello", params)
                print(f"接收到响应: {call_tool_result.content}")
    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    asyncio.run(async_sse_client("围城"))