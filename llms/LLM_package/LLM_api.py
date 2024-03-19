
import erniebot
from erniebot_agent.agents import FunctionAgent
from erniebot_agent.chat_models import ERNIEBot

from erniebot_agent.memory import HumanMessage, AIMessage, SystemMessage, FunctionMessage
import asyncio
from docx import Document
import time, json ,re
from tqdm import tqdm

from .LLM_prompt import *
from .utils import *

#子函数
async def analyse_topic(info, model):

    system_message = SystemMessage(content=analysis_prompt['system_message'])

    pre_text, item, answer = info['pretext'], info['content'], info['answer']
    human_messages = f"相关内容:{pre_text}\n题干:{item}\n参考答案:{answer}"

    messages = [HumanMessage(analysis_prompt['pre_human_message'] + human_messages)]
    #print(messages[0].content)

    #start = time.time()
    ai_message = await model.chat(messages=messages, system=system_message.content)
    #dur = time.time() - start

    #print(f"题目 耗时{dur:.2f}s\n {ai_message.content} ")
    output = ai_message.content.replace("```json", "").replace("```", "").replace("\n","").strip()
    dictionary = json.loads(output)

    return dictionary

def pre_exam(exam_path, answer_path, save_json_path, kdb_path):

    print("开始预处理试卷...")
    raw_exam_dict = load_exam(exam_path)
    answer_dict = load_answer(answer_path)

    exam_dict = add_answer_to_exam(raw_exam_dict, answer_dict)
    if not os.path.exists(kdb_path):
        os.makedirs(kdb_path)

    simplify_content(exam_dict, save_json_path, kdb_path)

#耗费toekn 预估 20w
async def llm_analysis_exam(exam_json_path, save_json_path):

    with open(exam_json_path, 'r', encoding='utf-8') as exam_json:
        exam_info = json.load(exam_json)

    model = ERNIEBot(model="ernie-4.0", temperature = 0.01)

    print("开始分析知识点...")

    for info in tqdm(exam_info.values()):
        if info["sub_topic"]:
            for sub_info in info["sub_topic"].values():
                sub_info['analysis'] = await analyse_topic(sub_info, model)
        else:
            info['analysis']  = await analyse_topic(info, model)

    print("知识点分析已完成！")

    with open(save_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(exam_info, json_file, ensure_ascii=False)






