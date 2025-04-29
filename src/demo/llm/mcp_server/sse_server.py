from mcp.server.fastmcp import FastMCP

# 创建一个MCP服务器
mcp = FastMCP("HelloWorld", port=9000)

@mcp.tool(name="hello", description="向指定的人打招呼")
# 流式输出
async def hello(name: str):
    return f"你好，{name}！"

if __name__ == "__main__":
    # 启动服务器
    mcp.run(transport='sse')