import os
from langchain.text_splitter import SpacyTextSplitter
#from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.documents import Document
from erniebot_agent.extensions.langchain.embeddings import ErnieEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import re, time

aistudio_access_token = os.environ.get("EB_AGENT_ACCESS_TOKEN")

def sanitize_filename(text):
    return re.sub(r'[\/:*?"<>|（），]', '', text)

class FaissSearch():
    def __init__(self, db, embeddings):
        # 类的初始化方法，接收一个数据库实例并将其存储在类的实例变量 self.db 中，接收一个embeddings方法传到self.embeddings中
        self.db = db
        self.embeddings = embeddings

    def search(self, query: str, top_k: int = 10, **kwargs):
        # 定义一个搜索方法，接受一个查询字符串 'query' 和一个整数 'top_k'，默认为 10
        docs = self.db.similarity_search(query, top_k)
        # 调用数据库的 similarity_search 方法来获取与查询最相关的文档
        para_result = self.embeddings.embed_documents([i.page_content for i in docs])
        # 对获取的文档内容进行嵌入（embedding），以便进行相似性比较
        query_result = self.embeddings.embed_query(query)
        # 对查询字符串也进行嵌入
        similarities = cosine_similarity([query_result], para_result).reshape((-1,))
        # 计算查询嵌入和文档嵌入之间的余弦相似度
        retrieval_results = []
        for index, doc in enumerate(docs):
            retrieval_results.append(
                {"content": doc.page_content, "score": similarities[index]} #"title": doc.metadata["source"]
            )
        # 遍历每个文档，将内容、相似度得分和来源标题作为字典添加到结果列表中
        return retrieval_results  # 返回包含搜索结果的列表

class LLm_KnowledgeBase():

    def __init__(self,
                 dbs_path,
                 thred,
                 chunk_size=150,
                 top_k = 4) -> None:
        
        self.cache_list = []
        self.dbs_path = dbs_path
        self.thred = thred
        self.chunk_size = chunk_size
        self.top_k = top_k
        self.embeddings =  ErnieEmbeddings(aistudio_access_token=aistudio_access_token, chunk_size=16)
    
    def get_faiss_db(self, db_name, text):

        if db_name not in self.cache_list:

            text_splitter = SpacyTextSplitter(pipeline="zh_core_web_sm", chunk_size=self.chunk_size, chunk_overlap=0)
            doc = Document(page_content=text)
            docs = text_splitter.split_documents([doc])
            db = FAISS.from_documents(docs, self.embeddings)
            db.save_local(self.dbs_path)

            self.cache_list.append(db_name)

        else:
            db = FAISS.load_local(self.dbs_path, self.embeddings, allow_dangerous_deserialization=True)

        return db


    def search(self, db, query_message):

        faiss_search = FaissSearch(db=db, embeddings=self.embeddings)
        
        res = faiss_search.search(query=query_message,top_k=self.top_k)
        content = ""
        for item_dict in res:
            if item_dict['score'] > self.thred:
                content += f"{item_dict['content']} \n....\n"
        return content
    
def demo():
    llm_kb = LLm_KnowledgeBase('knowledge_db',0.6,chunk_size=150)
    pretext, query = '', ''
    db = llm_kb.get_faiss_db(sanitize_filename(pretext.split('\n')[0]),pretext)
    content = llm_kb.search(db, query)

