from mcp import ClientSession
from mcp.client.sse import sse_client
from typing import Dict, Any
from .mcp_client import McpClient
from .tool import Tool


class SseMcpClient(McpClient):
    """使用SSE协议的MCP客户端实现"""
    
    def __init__(self, name: str, url: str):
        """
        初始化SSE MCP客户端
        
        Args:
            name: 客户端名称
            url: SSE服务器URL
        """
        super().__init__(name)
        self.url = url
        self.session = None
        self.stream_context = None
        self.available_tools = []

    async def connect(self) -> bool:
        """连接到MCP服务器"""
        try:
            # 创建一个新的sse_client上下文
            self.stream_context = sse_client(self.url)
            # 进入上下文并获取streams
            streams = await self.stream_context.__aenter__()
            # 创建并初始化会话
            self.session = ClientSession(*streams)
            await self.session.__aenter__()

            # 初始化连接
            capabilities = await self.session.initialize()
            print(f"已连接到服务器 {self.name}，功能: {capabilities}")

            # 获取可用工具
            tools_response = await self.session.list_tools()
            tools = []
            # 遍历工具响应，解析并存储工具信息
            for item in tools_response:
                if isinstance(item, tuple) and item[0] == 'tools':
                    for tool in item[1]:
                        tools.append(Tool(tool.name, tool.description, tool.inputSchema))
            self.available_tools = tools
            return True
        except Exception as e:
            print(f"连接失败: {e}")
            # 如果连接失败，确保清理资源
            await self.close()
            return False

    async def close(self) -> None:
        await super().close()
        # 然后关闭stream上下文
        if self.stream_context:
            try:
                await self.stream_context.__aexit__(None, None, None)
            except Exception as e:
                print(f"关闭流上下文时出错: {e}")
            finally:
                self.stream_context = None