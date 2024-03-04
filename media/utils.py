from docx import Document
from django.conf import settings
import os,sys,re
sys.path.append(os.path.abspath(__file__))
#print(settings)

document = Document(r'media\2020年全国卷Ⅰ语文高考试题.docx')  # 打开文件example.docx
current_key = None
content_dict = {}

for paragraph in document.paragraphs:
    if re.match(r'\d+．', paragraph.text):
        current_key = paragraph.text
        content_dict[current_key] = []
    elif current_key is not None:
        content_dict[current_key].append(paragraph.text)

# 将每个题目的段落列表合并成一个字符串
for key in content_dict:
    content_dict[key] = ' '.join(content_dict[key])

print(content_dict)