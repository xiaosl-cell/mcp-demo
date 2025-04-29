from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class McpClient(ABC):
    """
    MCP客户端抽象基类，定义了所有MCP客户端必须实现的接口
    """
    
    def __init__(self, name: str):
        """
        初始化MCP客户端
        
        Args:
            name: 客户端名称
        """
        self.name = name
        self.session = None
        self.available_tools = []
        
    @abstractmethod
    async def connect(self) -> bool:
        """
        连接到MCP服务器
        
        Returns:
            连接是否成功
        """
        pass
        
    async def call_tool(self, tool_name: str, params: Dict[str, Any]) -> Any:
        """
        调用MCP工具
        
        Args:
            tool_name: 工具名称
            params: 工具参数
            
        Returns:
            工具调用结果
        """
        """调用指定的工具"""
        if not self.session:
            print("未连接到服务器，请先调用connect()")
            return None

        try:
            result = await self.session.call_tool(tool_name, params)
            print(f"工具 {tool_name}, 参数：{params},结果: {result}")
            return result
        except Exception as e:
            print(f"调用工具 {tool_name} 失败: {e}")
            return None
        

    async def close(self) -> None:
        """
        关闭MCP连接
        """
        # 先关闭会话
        if self.session:
            try:
                await self.session.__aexit__(None, None, None)
            except Exception as e:
                print(f"关闭会话时出错: {e}")
            finally:
                self.session = None
        
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        获取可用工具列表
        
        Returns:
            可用工具列表
        """
        return self.available_tools