import asyncio
import os
import erniebot
from erniebot_agent.agents import FunctionAgent
from erniebot_agent.chat_models import ERNIEBot
from erniebot_agent.tools import RemoteToolkit
from erniebot_agent.memory import HumanMessage, AIMessage, SystemMessage, FunctionMessage
import asyncio
from .LLM_prompt import *

#import erniebot


def json2message(content):
    """用作后续的格式转换..保留内容"""

    return content

async def analysis_problem(inputs):
    """
    描述:
        - 针对某一道具体题目(包含学生作答)进行分析，并给出该题所含知识点以及评分建议。
    参数:
        - inputs: 题目内容(目前为字符串，后续可为json文件或者字典等形式)
    返回:
        - 文心一言的返回结果: str
    """

    system_message = SystemMessage(content=p_system_message)
    pre_prompt = p_analysis_pre
    #`_config_`, `top_p`, `temperature`,`penalty_score`, `system`
    paper_message = json2message(inputs)
    model = ERNIEBot(model="ernie-4.0", temperature = 0.01)

    messages = [HumanMessage(pre_prompt + paper_message)]
    
    #erniebot.api_type = 'aistudio'
    #erniebot.access_token = "864dc877bb527022d4e95ccbbc49cd471ea25f7b"
    ai_message = await model.chat(messages=messages, system=system_message.content, stream=True)
    count_tokens = 0
    async for chunk in ai_message:  # 流式输出结果
        count_tokens += chunk.token_count

        yield chunk.content

    #release版本删除print
    print("\n使用 tokens:", count_tokens)
        



