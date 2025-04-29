import json
import asyncio
import os
from config.mcp_config import McpConfig
from mcp_client import McpClient, SseMcpClient, StdioMcpClient
from llm_client import LLMClient

async def load_mcp_config(base_dir: str):
    """加载mcp配置"""
    config_path = os.path.join(base_dir, 'server_config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        mcp_config = json.load(f)
    mcp_config_list = []
    for name, config in mcp_config.get('mcpServers', {}).items():
        mcp_config_list.append(McpConfig(name, config))
    print(json.dumps([cfg.to_dict() for cfg in mcp_config_list], indent=2))
    return mcp_config_list


async def create_clients(base_dir: str, configs: list):
    clients = []
    for config in configs:
        if config.type == 'sse':
            # 创建SSE客户端
            client = SseMcpClient(config.name, config.url)
            clients.append(client)
        elif config.type == 'stdio':
            # 创建Stdio客户端
            full_args = []
            for arg in config.args:
                full_arg = os.path.join(base_dir, arg)
                full_args.append(full_arg)
            client = StdioMcpClient(config.name, config.command, full_args)
            clients.append(client)
        else:
            raise ValueError(f"Invalid client type: {config.type}")
        await client.connect()
    return clients


async def get_tool_descriptions(clients: list[McpClient]):
    all_tools = []
    for client in clients:
        tools = client.available_tools
        all_tools.extend(tools)
    return "\n".join([tool.format_for_llm() for tool in all_tools])


async def process_tool_call(tool_name, arguments, clients):
    """处理一次工具调用的完整流程"""
    # 1. 查找工具提供者
    target_client = await find_tool_provider(tool_name, clients)

    if not target_client:
        print(f"找不到工具 {tool_name} 的提供者")
        return None

    # 2. 调用工具
    return await target_client.call_tool(tool_name, arguments)


async def find_tool_provider(tool_name, clients):
    """查找工具的提供者客户端"""
    for client in clients:
        for tool in client.available_tools:
            if tool.name == tool_name:
                return client
    return None


async def update_messages_with_tool_result(messages, tool_name, arguments, tool_result):
    """将工具调用以及结果添加到消息列表中"""
    messages.append({
        "role": "assistant",
        "content": json.dumps(
            {
                "message_type": "tool_call",
                "tool": tool_name,
                "arguments": arguments
            }
        )
    })
    messages.append({"role": "user", "name": tool_name, "content": tool_result.content[0].text})
    return messages


async def get_llm_response(messages, llm_client):
    """获取LLM响应并解析"""
    response = llm_client.ask(messages)
    try:
        response_obj = json.loads(response)
        is_tool_call = 'message_type' in response_obj and response_obj['message_type'] == 'tool_call'
    except (json.JSONDecodeError, TypeError):
        # 如果不是JSON或没有正确字段，则视为普通文本响应
        print(response)
        response_obj = {"message_type": "final_answer", "result": response}
        is_tool_call = False

    return response_obj, is_tool_call


async def main():
    # 获取项目根目录
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    # 加载并解析MCP配置
    mcp_config_list = await load_mcp_config(base_dir)

    # 构造MCP客户端
    clients = await create_clients(base_dir, mcp_config_list)

    # 获取工具描述
    tools_description = await get_tool_descriptions(clients)

    # 读取提示词模板构造系统提示词
    prompt_path = os.path.join(base_dir, 'prompt', 'systemPrompt.txt')
    with open(prompt_path, 'r', encoding='utf-8') as f:
        system_message_template = f.read()
    system_message = system_message_template.replace("{tools_description}", tools_description)

    # 消息初始化
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": "16-(5+8)*2=?"}
    ]

    # 获取初始LLM响应
    llm_client = LLMClient()
    response_obj, is_tool_call = await get_llm_response(messages, llm_client)

    # 循环工具调用
    while is_tool_call:
        tool_name = response_obj['tool']
        arguments = response_obj['arguments']

        # 处理工具调用
        tool_result = await process_tool_call(tool_name, arguments, clients)

        # 3. 更新消息列表
        messages = await update_messages_with_tool_result(messages, tool_name, arguments, tool_result)

        # 4. 获取LLM响应
        response_obj, is_tool_call = await get_llm_response(messages, llm_client)

        if response_obj is None:
            break

    # 输出最终响应
    if 'result' in response_obj and response_obj['message_type'] == 'final_answer':
        print(response_obj['result'])
    else:
        print(json.dumps(response_obj, ensure_ascii=False, indent=2))

    # 关闭所有客户端连接
    for client in clients:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main()) 