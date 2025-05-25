# Phân Tích Mã Code

Đoạn mã Python này xây dựng một hệ thống truy vấn văn bản dựa trên vector hóa tài liệu, sử dụng các công cụ từ thư viện LangChain và FAISS để tải, xử lý, chia nhỏ, nhúng và tìm kiếm các đoạn văn bản liên quan đến truy vấn người dùng.

## Các Thành Phần Chính

### 1. Thư viện và Công cụ được sử dụng
- **`TextLoader` và `UnstructuredMarkdownLoader`**: Dùng để tải tài liệu từ các file văn bản thuần túy và file Markdown tương ứng.
- **`CharacterTextSplitter` và `RecursiveCharacterTextSplitter`**: Dùng để chia nhỏ tài liệu thành các đoạn nhỏ hơn với kích thước 1000 ký tự và chồng lấp 50 ký tự, giúp cho việc nhúng và tìm kiếm hiệu quả hơn.
- **`OpenAIEmbeddings`**: Tạo vector biểu diễn (embedding) cho các đoạn văn bản.
- **`FAISS`**: Thư viện lưu trữ và tìm kiếm vector nhanh, được dùng để xây dựng vectorstore và retriever.

### 2. Quy trình xử lý tài liệu
- Tải tài liệu từ file `reference.txt` bằng `TextLoader`.
- Chia nhỏ tài liệu này thành các đoạn (chunks) với `CharacterTextSplitter`.
- Tải tài liệu Markdown từ `example_doc.md` bằng `UnstructuredMarkdownLoader`.
- Chia nhỏ tài liệu Markdown với `RecursiveCharacterTextSplitter`.
- Kết hợp các đoạn văn từ cả hai tài liệu thành một danh sách chung `chunks`.

### 3. Tạo vectorstore và retriever
- Khởi tạo embeddings với `OpenAIEmbeddings`.
- Tạo vectorstore FAISS từ các đoạn văn bản đã chia nhỏ và nhúng.
- Tạo một retriever từ vectorstore với tham số tìm kiếm lấy 4 kết quả phù hợp nhất (`k=4`).

### 4. Hàm `retrieve_knowledge`
- Nhận đầu vào là một truy vấn dạng chuỗi.
- Sử dụng retriever để tìm các đoạn văn bản liên quan đến truy vấn.
- Trả về danh sách các nội dung văn bản phù hợp dưới dạng danh sách chuỗi.

## Mục Đích
Hệ thống này giúp người dùng có thể tìm kiếm thông tin liên quan trong các tài liệu văn bản một cách hiệu quả bằng cách sử dụng kỹ thuật vector hóa và tìm kiếm gần đúng (approximate nearest neighbor search).

---

## Mã nguồn gốc
```python
from typing import List
from langchain_community.document_loaders import TextLoader, UnstructuredMarkdownLoader  # type: ignore
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings  # type: ignore
from langchain_community.vectorstores import FAISS  # type: ignore

# Tạo retriever khi import module
loader = TextLoader("./docs/reference.txt")
docs = loader.load()
splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# Hoặc sử dụng UnstructuredMarkdownLoader nếu cần
loader = UnstructuredMarkdownLoader("./docs/example_doc.md")
docs_pattem = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
chunks_pattem = splitter.split_documents(docs_pattem)

# Kết hợp các đoạn văn bản từ cả hai tài liệu
chunks.extend(chunks_pattem)

# Tạo vectorstore và retriever
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

def retrieve_knowledge(query: str) -> List[str]:
    """Lấy các đoạn văn bản liên quan đến truy vấn."""
    results = retriever.get_relevant_documents(query)
    return [doc.page_content for doc in results]
```

Hy vọng với cách trình bày này, nội dung sẽ trở nên rõ ràng và dễ hiểu hơn cho người đọc!