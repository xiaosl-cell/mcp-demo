import os
from typing import Dict, Any, List, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from .mcp_client import McpClient
from .tool import Tool


class StdioMcpClient(McpClient):
    """使用标准输入输出的MCP客户端实现"""
    
    def __init__(self, name: str, command: str, args: List[str], env: Optional[Dict[str, str]] = None):
        """
        初始化Stdio MCP客户端
        
        Args:
            name: 客户端名称
            command: 执行命令 (如 'python')
            args: 命令参数列表
            env: 环境变量字典，默认为None使用当前环境
        """
        super().__init__(name)
        self.command = command
        self.args = args
        # 如果没有提供环境变量，使用当前环境并设置编码
        self.env = env if env is not None else os.environ.copy()
        self.stdio_context: Optional[Any] = None
        if "PYTHONIOENCODING" not in self.env:
            self.env["PYTHONIOENCODING"] = "utf-8"
        
        self.exit_stack = None
        self.stdio_transport = None
        
    async def connect(self) -> bool:
        """连接到MCP服务器"""
        try:
            # 设置服务器参数
            server_params = StdioServerParameters(
                command=self.command,
                args=self.args,
                env=self.env
            )
            
            # 创建一个新的退出栈
            from contextlib import AsyncExitStack
            self.exit_stack = AsyncExitStack()
            
            # 创建一个stdio_client
            self.stdio_context = stdio_client(server_params)
            read, write = await self.stdio_context.__aenter__()
            self.session = ClientSession(read, write)
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
        """关闭连接"""
        await super().close()

        # 然后关闭stream上下文
        if self.stdio_context:
            try:
                await self.stdio_context.__aexit__(None, None, None)
            except Exception as e:
                print(f"关闭流上下文时出错: {e}")
            finally:
                self.stdio_context = None
