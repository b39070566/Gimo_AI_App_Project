import logging
import json
from flask import Flask, jsonify, request
from anthropic import Anthropic
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 初始化 Anthropic 客戶端
api_key = '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'
anthropic_client = Anthropic(api_key=api_key)

# 初始化嵌入模型
embeddings = HuggingFaceEmbeddings(model_name="shibing624/text2vec-base-chinese-paraphrase")

# 全局變量存儲原始數據
raw_data = []

def initialize_vectorstore():
    global raw_data
    try:
        with open('history.json', 'r', encoding='utf-8') as file:
            raw_data = json.load(file)
        
        logger.info(f"原始數據樣本: {raw_data[:2]}")
        
        if not isinstance(raw_data, list):
            raise ValueError("預期在 JSON 文件中的是一個列表")
        
        documents = [Document(page_content=item, metadata={"id": i}) for i, item in enumerate(raw_data)]
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

def get_ai_response(question):
    try:
        if vectorstore is None or not raw_data:
            return "抱歉，系統當前無法處理您的請求。", []
        
        # 直接使用向量搜索
        relevant_docs = vectorstore.similarity_search(question, k=4)
        doc_contents = [doc.page_content for doc in relevant_docs]
        
        logger.info(f"檢索到的文檔，針對問題 '{question}': {doc_contents}")
        
        combined_info = " ".join(doc_contents)[:1000]
        
        response = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=150,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": f"基於此信息：{combined_info}\n控制在30字以內回應，回答以下問題：{question}(user_quest)"}
            ]
        )
        return response.content[0].text, doc_contents
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