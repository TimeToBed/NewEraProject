
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
async def item_mark(info, model):

    system_message = SystemMessage(content=mark_prompt['system_message'])

    human_messages = f"原题:{info['content']}\题目分值:{info['score']}\n原题及学生作答:{info['ocr_content']}\n参考解析:{info['analysis']}"

    messages = [HumanMessage(human_messages)]

    ai_message = await model.chat(messages=messages, system=system_message.content)

    output = ai_message.content.replace("```json", "").replace("```", "").replace("\n","").strip()
    dictionary = json.loads(output)

    return dictionary

async def llm_mark_test(llm_premark_json, save_json_path):

    with open(llm_premark_json, 'r', encoding='utf-8') as f:
        premark_info = json.load(f)

    model = ERNIEBot(model="ernie-4.0", temperature = 0.01)

    print("开始文心一言的批阅...")

    for k_fst,v_fst in tqdm(premark_info.items()):

        if k_fst in ["姓名","学号"]: continue
        for k_sec,v_sec in v_fst.items():
            #此时为 四、{"11":{}..}的格式
            if k_sec.isdigit():
                if 'score' in v_sec:
                    result = await item_mark(v_sec, model)
                    premark_info[k_fst][k_sec]['llm_mark'] = result['score']
                    premark_info[k_fst][k_sec]['llm_comment'] = result['comment']
                else:
                    for k_sub, v_sub in v_sec:
                        result = await item_mark(v_sub, model)
                        premark_info[k_fst][k_sec][k_sub]['llm_mark'] = result['score']
                        premark_info[k_fst][k_sec][k_sub]['llm_comment'] = result['comment']

            #此时为 二、{"（一）":{"5":{..},"6":{}.}..}的格式
            else:
                for k_thrd,v_thrd in v_sec.itmes():
                    if 'score' in v_thrd:
                        result = await item_mark(v_thrd, model)
                        premark_info[k_fst][k_sec][k_thrd]['llm_mark'] = result['score']
                        premark_info[k_fst][k_sec][k_thrd]['llm_comment'] = result['comment']
                    else:
                        for k_sub, v_sub in v_sec:
                            result = await item_mark(v_sub, model)
                            premark_info[k_fst][k_sec][k_thrd][k_sub]['llm_mark'] = result['score']
                            premark_info[k_fst][k_sec][k_thrd][k_sub]['llm_comment'] = result['comment']

    print("文心一言的批阅完成...")

    with open(save_json_path, 'w', encoding='utf-8') as f:
        json.dump(premark_info, f, ensure_ascii=False)


async def llm_mark(llm_premark_json):

    async def handle_item(paths, item, model):
        result = await item_mark(item, model)
        print(result)

        dict_obj = premark_info
        try:
            for p in paths:
                dict_obj = dict_obj[p]
            dict_obj['llm_mark'] = result['score']
            dict_obj['llm_comment'] = result['comment']
        except KeyError:
            print("KeyError for paths: ", paths)
            return 
    
    with open(llm_premark_json, 'r', encoding='utf-8') as f:
        premark_info = json.load(f)

    model = ERNIEBot(model="ernie-4.0", temperature=0.01)

    print("开始文心一言的批阅...")

    for k_fst, v_fst in tqdm(premark_info.items()):
        if k_fst in ["姓名","学号","四"]: continue
        for k_sec, v_sec in v_fst.items():
            if k_sec.isdigit():

                if 'score' in v_sec:
                    await handle_item([k_fst, k_sec], v_sec, model)
                else:
                    for k_sub, v_sub in v_sec.items():
                        await handle_item([k_fst, k_sec, k_sub], v_sub, model)
            else:

                for k_thrd, v_thrd in v_sec.items():
                    if 'score' in v_thrd:
                        await handle_item([k_fst, k_sec, k_thrd], v_thrd, model)
                    else:
                        for k_sub, v_sub in v_thrd.items():
                            await handle_item([k_fst, k_sec, k_thrd, k_sub], v_sub, model)

    print("文心一言批阅结束...")
    with open(llm_premark_json, 'w', encoding='utf-8') as f:
        json.dump(premark_info, f, ensure_ascii=False)
    print("缓存成功！")

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






