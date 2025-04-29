class McpConfig:
    # 构造器输出一个字典，包含所有配置项
    def __init__(self, name: str ,config):
        self.type = config.get('type')
        self.name = name
        self.command = None
        self.args = None
        self.url = None
        if self.type == 'sse':
            self.url = config.get('url')
            if not self.url:
                raise ValueError('url is required for sse type')
        elif self.type == 'stdio':
            self.command = config.get('command')
            self.args = config.get('args')
            if not self.command or not self.args:
                raise ValueError('command and args are required for stdio type')
        else:
            raise ValueError('Invalid type')

    def __str__(self):
        return f"McpConfig(type={self.type}, name={self.name}, url={self.url}, command={self.command}, args={self.args})"
    
    def to_dict(self):
        return {
            'type': self.type,
            'name': self.name,
            'url': self.url,
            'command': self.command,
            'args': self.args
        }