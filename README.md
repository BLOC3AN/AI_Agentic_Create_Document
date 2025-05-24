## A2A Agents Nội Bộ trên LangChain + RAG

### 📁 Cấu trúc thư mục dự án

```
project_root/
├── docs/
│   └── reference.txt     # Tài liệu tham khảo cho RAG
├── tools/
│   ├── __init__.py       # empty file
│   ├── retrieve.py       # định nghĩa retrieve_knowledge
│   ├── analyze.py        # định nghĩa analyze_code
│   ├── write.py          # định nghĩa write_doc
│   └── save.py           # định nghĩa save_file
├── agent.py              # Khởi tạo LangChain agent và tools
└── main.py               # Script chạy ví dụ (import agent từ agent.py)
```
---
## File: docs/reference.txt
```
# Thư mục này chứa tài liệu hướng dẫn, best practices, ví dụ code, ...

# Ví dụ:

Python recursion uses call stack. For factorial, use base case n==0.
Describe how AST parsing works in Python.

````

## File: tools/retrieve.py

```python
from typing import List
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# Tạo retriever khi import module
loader = TextLoader("./docs/reference.txt")
docs = loader.load()
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})


def retrieve_knowledge(query: str) -> List[str]:
    """Lấy các đoạn văn bản liên quan đến truy vấn."""
    results = retriever.get_relevant_documents(query)
    return [doc.page_content for doc in results]
````

## File: tools/analyze.py

```python
from typing import Any, Dict, List
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model_name="gpt-4o-mini")

def analyze_code(code: str, context: List[str]) -> Dict[str, Any]:
    """Phân tích code kết hợp context và LLM, trả về JSON."""
    prompt = (
        "Bạn là chuyên gia Python. Dưới đây là code và kiến thức tham khảo:
"
        f"Context:
{context}
Code:
{code}
"
        "Hãy phân tích chi tiết và trả về JSON với keys: functions, analysis."
    )
    resp = llm.call_as_llm([{"role": "user", "content": prompt}])
    # Kết quả là một chuỗi JSON, parse nó nếu cần
    return resp
```

## File: tools/write.py

```python
from typing import List
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model_name="gpt-4o-mini")

def write_doc(analysis: str, context: List[str]) -> str:
    """Tạo Markdown từ analysis và context."""
    prompt = (
        "Bạn là technical writer. Kết hợp analysis và context để tạo Markdown đầy đủ:
"
        f"Context:
{context}
Analysis:
{analysis}
"
    )
    resp = llm.call_as_llm([{"role": "user", "content": prompt}])
    return resp
```

## File: tools/save.py

```python
import time

def save_file(markdown: str) -> str:
    """Lưu markdown vào file và trả về đường dẫn."""
    filename = f"output_{int(time.time())}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown)
    return filename
```

## File: agent.py

```python
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from tools.retrieve import retrieve_knowledge
from tools.analyze import analyze_code
from tools.write import write_doc
from tools.save import save_file

# Khởi tạo LLM
tool_llm = ChatOpenAI(model_name="gpt-4o-mini")

# Đăng ký tools
tools = [
    Tool(name="retrieve_knowledge", func=retrieve_knowledge, description="Lấy kiến thức liên quan từ docs"),
    Tool(name="analyze_code", func=analyze_code, description="Phân tích code với context"),
    Tool(name="write_doc", func=write_doc, description="Chuyển analysis thành Markdown"),
    Tool(name="save_file", func=save_file, description="Lưu Markdown vào file")
]

# Tạo agent
tag_agent = initialize_agent(
    tools,
    tool_llm,
    agent="zero-shot-react-description",
    verbose=True
)
```

## File: main.py

```python
from agent import tag_agent as agent
from tools.retrieve import retrieve_knowledge

if __name__ == "__main__":
    code_sample = '''
# Tính giai thừa
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)
    '''

    # 1. Lấy context
    ctx = retrieve_knowledge("Python recursion patterns and factorial implementation")

    # 2. Gửi prompt
    prompt = (
        "Phân tích code sau, dùng context để cải thiện độ chính xác, " 
        "viết tài liệu và lưu file:
" + code_sample
    )
    result = agent.run(prompt)
    print("Kết quả:", result)
```
