# MCP服务器演示项目

## 项目简介

这是一个基于MCP（Model Calling Protocol）的服务器演示项目，用于展示如何构建和使用MCP服务，实现大模型与工具的交互集成。该项目主要演示了如何创建MCP服务器、构建MCP客户端，以及如何利用LLM（大型语言模型）进行工具调用和编排。

## 项目结构

```
mcp-demo/
├── prompt/                  # 提示词模板
│   └── systemPrompt.txt     # 系统提示词
├── src/                     # 源代码
│   └── demo/
│       ├── llm/             # LLM与MCP集成的核心代码
│       │   ├── config/      # 配置相关
│       │   ├── llm/         # LLM客户端实现
│       │   ├── mcp_client/  # MCP客户端实现
│       │   ├── mcp_server/  # MCP服务器实现
│       │   └── host.py      # 主程序入口
│       ├── 1-stdio/         # 标准输入输出方式的MCP演示
│       └── 2-sse/           # SSE方式的MCP演示
├── server_config.json       # 服务器配置文件
└── requirements.txt         # 项目依赖
```

## 安装方法

1. 克隆仓库并进入项目目录
2. 安装依赖包

```bash
pip install -r requirements.txt
```

## 功能特性

- 支持多种MCP通信方式：
  - 标准输入/输出 (stdio)
  - 服务器发送事件 (SSE)
- 提供基本计算工具服务
- 支持大模型工具调用与编排
- 可扩展的工具注册机制

## 使用方法

### 配置LLM
在项目根目录创建`.env`文件,配置以下环境变量:

### OpenAI API密钥
LLM_API_KEY=your_api_key
LLM_BASE_URL=proxy_base_url
MODEL=gpt-4o


### 运行示例

执行主程序：
1-stdio：python ${项目完整路径}/src/demo/1-stdio/stdio_client.py}
2-sse:
  - python ${项目完整路径}/src/demo/2-sse/sse_server.py
  - python ${项目完整路径}/src/demo/2-sse/sse_client.py
llm: python ${项目完整路径}/src/demo/llm/host.py


### 自定义MCP服务

您可以在`mcp_server`目录下创建自己的MCP服务器，例如：

```python
from mcp.server.fastmcp import FastMCP

# 创建一个MCP服务器
mcp = FastMCP("自定义服务名称")

@mcp.tool(name="tool_name", description="工具描述")
async def tool_function(param1: type, param2: type) -> return_type:
    # 实现工具逻辑
    return result

if __name__ == "__main__":
    # 启动服务器
    mcp.run()
```

### 配置MCP服务
编辑`server_config.json`文件，配置MCP服务器：

```json
{
  "mcpServers": {
    "Calculation": {
      "type": "stdio",
      "command": "python",
      "args": ["${项目完整路径}/stdio_server.py"]
    }
  }
}
```

type: 支持stdio,sse
command: 执行命令 stdio模式必填
args: 执行命令参数 stdio模式必填
url: 服务地址 sse模式必填


## 依赖项

- mcp >= 1.2.0
- openai >= 1.10.0
- asyncio >= 3.4.3
- python-dotenv >= 1.0.0

## 许可证

本项目遵循[许可证名称]开源许可。 