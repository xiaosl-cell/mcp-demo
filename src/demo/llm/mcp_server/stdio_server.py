from mcp.server.fastmcp import FastMCP

# 创建一个MCP服务器
mcp = FastMCP("Calculation")

@mcp.tool(name="add", description="计算两数之和")
async def add(a: float, b: float) -> float:
    return a + b

@mcp.tool(name="subtract", description="计算两数之差")
async def subtract(a: float, b: float) -> float:
    return a - b

@mcp.tool(name="multiply", description="计算两数之积")
async def multiply(a: float, b: float) -> float:
    return a * b

@mcp.tool(name="divide", description="计算两数之商")
async def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b

if __name__ == "__main__":
    # 启动服务器
    mcp.run()