from mcp.server.fastmcp import FastMCP

# 创建一个MCP服务器
mcp = FastMCP("HelloWorld")

@mcp.tool()
def hello(name: str) -> str:
    """向指定的人打招呼"""
    return f"你好，{name}！"

if __name__ == "__main__":
    # 启动服务器
    mcp.run()