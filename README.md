
---

# Gimo AI App Project

## 專案簡介

本專案是一個結合「歷史劇情遊戲」與「生成式 AI 問答系統」的應用，目標是在遊戲情境中提供即時的知識輔助，讓使用者在互動過程中完成學習。

與一般問答系統不同，本系統將 AI 嵌入在遊戲敘事流程中，使模型能根據當下劇情提供更具情境性的回應，而非單純的事實查詢。

---

## 核心概念

本專案的設計重點在於將 AI 從單純的問答工具，轉換為具備情境感知能力的教學輔助系統。

整體流程可分為三個部分：

* 遊戲提供情境（Context）
* 檢索系統提供知識依據（Retrieval）
* 語言模型負責生成回應（Generation）

透過這樣的架構，讓回答不僅正確，也能貼合遊戲中的對話脈絡。

---

## 專案亮點

### 跨系統整合

本專案整合了遊戲引擎、後端 API、向量檢索與大型語言模型，建立完整的資料流：

Game Client → API Server → Retrieval → LLM → Response → Game

重點不只是模型本身，而是整體系統如何協同運作。

---

### RAG 架構實作

使用 Retrieval-Augmented Generation（RAG）提升回答品質：

* 透過向量檢索取得相關歷史資料
* 將檢索結果作為 Prompt context
* 降低模型產生錯誤資訊（hallucination）的機率

這部分是整個系統可靠性的關鍵。

---

### 中文語境優化

針對中文歷史內容進行調整：

* 使用中文語意 embedding 模型
* 設計偏教學導向的 prompt
* 回答風格以「解釋 + 引導」為主

使輸出更接近實際教學場景，而不是單純生成答案。

---

### 可擴展的知識架構

知識來源以 JSON 格式管理，具備良好的擴展性：

* 可替換不同主題（如台灣史 / 世界史）
* 可快速擴充資料集
* 不需修改核心程式即可調整內容

---

## 功能說明

### 劇情互動系統（Ren'Py）

* 提供角色對話與劇情推進
* 在特定節點觸發問答
* 將問題透過 HTTP 傳送至後端
* 將 AI 回應即時呈現在遊戲對話中

這部分的重點在於將 AI 整合進 narrative flow，而不是額外功能。

---

### AI 問答 API（Flask）

提供簡單的 REST API：

GET /ask?question=...

處理流程：

1. 接收使用者問題
2. 轉換為向量表示
3. 進行相似度檢索（FAISS）
4. 組合 Prompt（context + query）
5. 呼叫 LLM 生成回答
6. 回傳結果

回傳格式：

```json
{
  "answer": "AI 生成回答",
  "retrieved_docs": ["相關歷史片段"]
}
```

---

### RAG Pipeline

系統核心流程如下：

User Query
→ Embedding
→ Vector Search（Top-K）
→ Context Construction
→ LLM
→ Answer

實作重點：

* 使用 HuggingFace Embeddings 建立向量
* 使用 FAISS 作為向量資料庫
* 採用 Top-K 檢索提升相關性

---

## 系統架構

```
[Ren'Py Game Client]
        ↓
[Flask API Server]
        ↓
[FAISS Vector Database]
        ↓
[LLM Service]
        ↓
[Response 回傳至遊戲]
```

---

## 技術棧

Frontend / Game

* Ren'Py

Backend

* Flask

AI / NLP

* Claude（LLM）
* HuggingFace Embeddings

Retrieval

* LangChain
* FAISS

---

## 設計思考

這個專案的重點不在於單一技術，而在於：

* 如何讓 AI 真正融入應用場景
* 如何透過 RAG 提升系統可信度
* 如何設計一個可擴展的知識系統

相較於純聊天機器人，本系統更偏向「任務導向 + 情境導向」的 AI 應用。

---

