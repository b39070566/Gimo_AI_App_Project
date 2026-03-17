我幫你把這份 README 做成「**更有層次 + 更偏研究/面試導向 + 更專業敘事**」的版本（重點是讓教授/面試官一看就覺得你是有在做系統設計的人）👇

---

# 🎮 Gimo AI App Project

> **面試作品說明**
> 本專案為一個結合「**歷史劇情遊戲 × AI 教學問答系統**」的跨領域應用，透過將生成式 AI 嵌入遊戲情境，打造沉浸式互動學習體驗（Game-based Learning + LLM）。

---

##  專案核心概念

本系統的核心設計理念為：

> **將 AI 從「被動問答工具」轉化為「情境式教學代理人（Context-aware Tutor）」**

透過：

* 劇情遊戲提供情境（Context）
* RAG 提供知識支撐（Knowledge Grounding）
* LLM 負責自然語言生成（Response Generation）

實現「邊玩邊學」的互動式學習模式。

---

## 專案亮點（面試官重點🔥）

### 跨系統整合能力

* 整合 **Ren'Py 遊戲引擎 + Flask API + LLM + 向量資料庫**
* 建立完整的「前端互動 → 後端推理 → 回傳結果」資料流

---

### RAG（Retrieval-Augmented Generation）架構

* 使用向量檢索（FAISS）提升回答準確度
* 避免 LLM 幻覺（Hallucination）
* 回答基於「歷史資料 + 語境提示」生成

---

### 中文歷史教學優化

* 採用中文語意 embedding 模型
* 設計教學導向 Prompt（引導式回答）
* 回答風格偏向「解釋 + 引導思考」

---

### 可擴展知識架構

* 使用 `history.json` 作為知識來源
* 支援快速：

  * 替換主題（如世界史 / 台灣史）
  * 擴充題庫
  * 客製教學內容

---

## 功能說明

### 劇情互動系統（Ren'Py）

* 提供角色對話、場景切換與章節推進
* 玩家可於劇情中觸發「歷史問答」
* 將問題透過 HTTP 傳送至後端 AI 系統
* 即時將 AI 回應整合回遊戲對話中

 本質：**將 AI 融入 Narrative Flow（敘事流程）**

---

### AI 問答 API（Flask）

* 提供：

  ```
  GET /ask?question=...
  ```

* 處理流程：

  1. 接收使用者問題
  2. 向量檢索相關歷史片段
  3. 組合 Prompt（Context + Query）
  4. 呼叫 LLM 生成回答
  5. 回傳 JSON 結果

* 回傳格式：

```json
{
  "answer": "AI 生成回答",
  "retrieved_docs": ["相關歷史片段"]
}
```

---

### 檢索增強生成（RAG Pipeline）

**技術流程：**

```text
User Query
   ↓
Embedding（HuggingFace）
   ↓
Vector Search（FAISS）
   ↓
Top-K Documents
   ↓
Prompt Construction
   ↓
LLM（Claude）
   ↓
Answer
```

**實作細節：**

* 使用 `HuggingFaceEmbeddings` 建立語意向量
* 使用 `FAISS` 建立高效向量索引
* 採 Top-K 檢索提升語境相關性

---

## 系統架構

```text
[Ren'Py Game Client]
        ↓ HTTP Request
[Flask API Server]
        ↓
[Vector Database (FAISS)]
        ↓
[LLM (Claude)]
        ↓
[Response → Game UI]
```

---

## 技術棧 (Tech Stack)

### 前端 / 遊戲層

* Ren'Py（視覺小說引擎）

###  後端

* Flask（API Server）

### AI / NLP

* Anthropic Claude（LLM）
* HuggingFace Embeddings（中文語意向量）

###  檢索系統

* LangChain
* FAISS（向量資料庫）

---

##  專案結構

```text
.
├── game/                      # Ren'Py 遊戲腳本與素材
├── Renpy2Flask-main/
│   ├── app.py                # Flask API + RAG 主邏輯
│   ├── history.json          # 歷史知識庫
│   └── requirements.txt
├── project.json              # Ren'Py 專案設定
```

---

##  快速啟動

###  啟動後端 API

```bash
cd Renpy2Flask-main
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

預設服務：

```
http://127.0.0.1:8000
```

---

###  測試 API

```bash
curl "http://127.0.0.1:8000/ask?question=西安事變是什麼"
```

---

##  範例回應

```json
{
  "answer": "西安事變促成國共第二次合作，對抗日本侵略。",
  "retrieved_docs": [
    "西安事變發生於1936年...",
    "張學良與楊虎城..."
  ]
}
```

---



https://github.com/b39070566/license/blob/main/license
