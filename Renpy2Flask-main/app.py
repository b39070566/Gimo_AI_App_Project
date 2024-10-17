import logging
import json
from flask import Flask, jsonify, request
from anthropic import Anthropic
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from fuzzywuzzy import fuzz  # 用於模糊匹配
from nltk.corpus import wordnet  # 用於同義詞處理
import nltk
nltk.download('wordnet')


# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 初始化 Anthropic 客戶端
api_key = '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'
anthropic_client = Anthropic(api_key=api_key)

# 初始化嵌入模型
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 全局變量存儲原始數據
raw_data = []

def initialize_vectorstore():
    global raw_data
    try:
        with open('history.json', 'r', encoding='utf-8') as file:
            raw_data = json.load(file)
        
        logger.info(f"原始數據樣本: {raw_data[:2]}")  # 只打印前兩條數據
        
        if not isinstance(raw_data, list):
            raise ValueError("預期在 JSON 文件中的是一個列表")
        
        # 創建文檔，不進行分割
        documents = [Document(page_content=item, metadata={"id": i}) for i, item in enumerate(raw_data)]
        
        # 創建 FAISS 索引
        vectorstore = FAISS.from_documents(documents, embeddings)
        
        return vectorstore
    except Exception as e:
        logger.error(f"初始化向量存儲時發生錯誤: {str(e)}")
        raise

# 初始化向量存儲
try:
    vectorstore = initialize_vectorstore()
except Exception as e:
    logger.error(f"無法初始化向量存儲: {str(e)}")
    vectorstore = None

SYSTEM_PROMPT = """
你是一位歷史小老師，在歷史教育遊戲中回答問題，但也可以回答一些公民類、地理位置。請遵循以下指導原則:
1. 友好、耐心地回答問題，像教導學生一樣。
1.2 請務必也要回答學生關於地理位置的相關問題，以求全面性了解
2. 更加專注於歷史主題，避免無關話題。
3. 保持專業感。
4. 主題涵蓋與台灣、中國相關的所有歷史。
5. 你面對的是遊戲軟體的使用者。
6. 如檢索資料中沒有相關信息，拒絕回答問題。
7. 將使用者視為客戶，不透露後台信息。
8. 不要說"根據提供的訊息"。
9. 回答不要分段。
10. 回答控制在30字內。
11. 拒絕回答歷史跟地理、公民以外的問題，回復"我只能回答歷史問題"。
"""

def get_synonyms(word):
    """返回同義詞列表"""
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return synonyms

def keyword_search(query, data, top_k=3):
    query_lower = query.lower()
    scored_results = []
    
    # 處理同義詞擴展
    query_words = query_lower.split()
    extended_query_words = set(query_words)
    for word in query_words:
        extended_query_words.update(get_synonyms(word))
    
    for item in data:
        score = 0
        content_lower = item.lower()
        
        # 提取前10個字，避免過短文本導致錯誤
        first_10_words = " ".join(content_lower.split()[:10])
        
        # 模糊匹配得分
        fuzzy_score = fuzz.partial_ratio(query_lower, content_lower)
        score += fuzzy_score
        
        # 前10個字完全匹配得更高分
        if query_lower in first_10_words:
            score += 200  # 為前10個字的匹配設置高分
        
        # 遍歷查詢中的擴展詞集，部分匹配也得分
        for word in extended_query_words:
            if word in content_lower:
                score += 50
        
        # 考慮文檔長度，但減少長度的影響
        score += min(len(content_lower) / 500, 10)  # 最多加10分
        
        if score > 0:
            scored_results.append((item, score))
    
    # 根據分數排序
    scored_results.sort(key=lambda x: x[1], reverse=True)
    
    return [item for item, _ in scored_results[:top_k]]

def hybrid_search(query, vectorstore, raw_data, top_k=2):
    # 向量搜索
    vector_results = vectorstore.similarity_search(query, k=top_k*2)
    vector_docs = [doc.page_content for doc in vector_results]
    
    # 關鍵詞搜索
    keyword_results = keyword_search(query, raw_data, top_k=top_k*2)
    
    # 合併結果
    combined_results = list(set(vector_docs + keyword_results))
    
    # 重新評分
    scored_results = []
    query_lower = query.lower()
    for doc in combined_results:
        score = 0
        content_lower = doc.lower()
        
        # 向量搜索結果得分
        if doc in vector_docs:
            score += 50
        
        # 關鍵詞匹配得分
        if query_lower in content_lower:
            score += 100
        for word in query_lower.split():
            if word in content_lower:
                score += 10
        
        # 輕微考慮文檔長度
        score += min(len(content_lower) / 1000, 5)  # 最多加5分
        
        scored_results.append((doc, score))
    
    # 根據分數排序
    scored_results.sort(key=lambda x: x[1])
    
    return [item for item, _ in scored_results[:top_k]]

def get_ai_response(question):
    try:
        if vectorstore is None or not raw_data:
            return "抱歉，系統當前無法處理您的請求。", []
        
        # 使用混合搜索
        relevant_docs = hybrid_search(question, vectorstore, raw_data, top_k=4)
        
        logger.info(f"檢索到的文檔，針對問題 '{question}': {relevant_docs}")
        
        combined_info = " ".join(relevant_docs)[:1000]  # 限制在1000字符以內
        
        response = anthropic_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=150,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": f"基於此信息：{combined_info}\n控制在30字以內回應，回答以下問題：{question}(user_quest)"}
            ]
        )
        return response.content[0].text, relevant_docs
    except Exception as e:
        logger.error(f"生成 AI 回應時發生錯誤: {str(e)}")
        return "抱歉，生成回應時發生錯誤。", []

@app.route('/ask', methods=['GET'])
def ask_question():
    user_question = request.args.get('question', '')
    logger.info(f"接收到問題: {user_question}")
    
    try:
        answer, retrieved_docs = get_ai_response(user_question)
        return jsonify({
            'answer': answer,
            'retrieved_docs': retrieved_docs
        })
    except Exception as e:
        logger.error(f"處理請求時發生錯誤: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)
