from __future__ import annotations

from typing import Any, Dict, Type, List
from pydantic import Field
from erniebot_agent.tools.base import Tool

from erniebot_agent.tools.schema import ToolParameterView



class SeparateInput(ToolParameterView):
    index: str = Field(description="待添加的小题号以及分题号")

class SeparateOutput(ToolParameterView):
    result: str = Field(description="从内容中提取出小题号或分题号，包括多种形式，例如‘（1） （2）’等")


class SeparateIndexTool(Tool):
    description: str = "将所有小题号以及分题号从该题中提取出来，并将其添加到列表中"
    input_type: Type[ToolParameterView] = SeparateInput
    ouptut_type: Type[ToolParameterView] = SeparateOutput

    def __init__(self) -> None:
        self.index_list = []
        super().__init__()

    async def __call__(self, index: str) -> Dict[str, Any]:
        self.index_list.append(index)
        descr = "\n".join(self.index_list)
        return {"result": f"当前内容中包含题号:{self.index_list}"}
