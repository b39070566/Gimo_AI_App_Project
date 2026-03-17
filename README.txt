# Gimo AI App Project

> 面試作品說明：這是一個「**歷史劇情遊戲 + AI 教學問答**」的跨領域整合專案，目標是讓玩家在遊戲情境中互動學習歷史。

## 專案亮點（給面試官）

- **遊戲與 AI 後端整合**：以 Ren'Py 劇情遊戲承載教學情境，串接 Flask API 提供即時問答。
- **RAG 檢索式問答流程**：先用向量檢索擷取歷史資料，再交由 LLM 組織成短答覆，提升回覆相關性。
- **中文歷史教學場景優化**：採用中文 embedding 模型與歷史語境提示詞，回答風格偏向「教學引導」。
- **可擴充的內容架構**：資料來源採 `history.json`，可快速替換題庫或擴充不同歷史主題。

## 功能介紹

### 1) 劇情遊戲互動（Ren'Py）

- 遊戲端包含角色對話、章節推進與場景顯示。
- 玩家在遊戲中可觸發「地點/人物相關」資訊查詢流程。
- 透過 HTTP 呼叫後端 API，將 AI 回答回饋到遊戲介面。

### 2) AI 問答 API（Flask）

- 提供 `GET /ask` 端點，接收玩家問題。
- 後端先進行向量相似度檢索（FAISS）。
- 將檢索內容與系統提示詞組合後送入 Claude 生成答案。
- 回傳內容包含：
  - `answer`：AI 最終回答
  - `retrieved_docs`：檢索到的參考片段（便於除錯與驗證）

### 3) 檢索增強生成（RAG）

- 使用 `HuggingFaceEmbeddings` 建立中文語意向量。
- 使用 `langchain_community.vectorstores.FAISS` 建立向量索引。
- 查詢時取前幾筆相關內容，提升回答與歷史題材的一致性。

## 系統架構

1. 玩家在 Ren'Py 遊戲提出問題。
2. 遊戲端向 Flask API 發送請求。
3. API 讀取向量庫進行相似度檢索。
4. 後端呼叫 LLM 生成精簡答案。
5. 回答結果回傳遊戲，形成即時教學互動。

## 技術棧

- **前端/遊戲引擎**：Ren'Py
- **後端框架**：Flask
- **LLM 服務**：Anthropic Claude
- **向量檢索**：LangChain + FAISS
- **語意嵌入模型**：HuggingFace（中文模型）

## 專案結構

- `game/`：Ren'Py 劇情腳本、角色、UI 與素材。
- `Renpy2Flask-main/app.py`：Flask API、向量檢索與 LLM 呼叫主程式。
- `Renpy2Flask-main/history.json`：歷史知識資料來源。
- `project.json`：Ren'Py 專案建置設定。

## 快速啟動（後端）

```bash
cd Renpy2Flask-main
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

服務預設啟動於：`http://127.0.0.1:8000`

## API 範例

```bash
curl "http://127.0.0.1:8000/ask?question=西安事變是什麼"
```

示意回應：

```json
{
  "answer": "西安事變促成國共第二次合作",
  "retrieved_docs": ["...", "..."]
}
```

## 我在這個專案展現的能力

- **跨模組整合能力**：將遊戲引擎、後端 API、LLM 與向量資料流串成可運作產品。
- **AI 應用落地能力**：不是只呼叫模型，而是加入檢索層提高內容可用性。
- **產品思維**：以「教育互動」為核心，將 AI 能力嵌入使用者旅程。
- **工程可維護性意識**：模組拆分清楚（遊戲端/後端端點/資料來源）。

## License

目前授權資訊可參考 `README.txt` 內提供的外部連結。

https://github.com/b39070566/license/blob/main/license
