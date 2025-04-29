import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client



# 创建服务器参数
server_params = StdioServerParameters(
    # 服务器执行的命令，这里是 python
    command="python",
    # 启动命令的附加参数，这里是运行 stdio_server.py
    args=["stdio_server.py"],
)

async def main():
    # 创建与服务器的标准输入/输出连接，并返回 read 和 write 流
    async with stdio_client(server_params) as (read, write):
        # 创建一个客户端会话对象，通过 read 和 write 流与服务器交互
        async with ClientSession(read, write) as session:
            # 向服务器发送初始化请求，确保连接准备就绪
            # 建立初始状态，并让服务器返回其功能和版本信息
            capabilities = await session.initialize()
            print("capabilities:", capabilities)

            # MCP工具集合
            tools = await session.list_tools()
            print("tools:", tools)

            # MCP Server调用
            result = await session.call_tool("hello", {"name": "围城"})
            print(f"result: {result}")



if __name__ == "__main__":
    asyncio.run(main()) 