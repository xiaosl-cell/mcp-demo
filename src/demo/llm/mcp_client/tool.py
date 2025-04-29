from typing import Dict, Any


class Tool:
    def __init__(self, name: str, description: str, input_schema: Dict[str, Any]) -> None:
        self.name: str = name
        self.description: str = description
        self.input_schema: Dict[str, Any] = input_schema

    def format_for_llm(self) -> str:
        args_desc = self.input_schema
        return f"""
                Tool: {self.name}
                Description: {self.description}
                Arguments:
                {args_desc}
                """