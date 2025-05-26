# Phân Tích Mã Code Python

Mã code Python này xây dựng một hệ thống tìm kiếm thông tin dựa trên nội dung tài liệu, với các bước chính như sau:

## Tổng Quan

- **Tải dữ liệu** từ các file văn bản và Markdown.
- **Chia nhỏ nội dung** thành các đoạn nhỏ để dễ xử lý.
- **Tạo vector biểu diễn (embedding)** cho các đoạn văn bản.
- **Xây dựng hệ thống tìm kiếm** dựa trên vector (vectorstore).
- **Cung cấp hàm truy vấn** để lấy các đoạn văn bản liên quan đến câu hỏi.

## Chi Tiết Các Bước

1. **Tải dữ liệu:**
   - Sử dụng `TextLoader` để tải nội dung từ file `./docs/reference.txt`.
   - Sử dụng `UnstructuredMarkdownLoader` để tải nội dung từ file Markdown `./docs/example_doc.md`.

2. **Chia nhỏ văn bản:**
   - Với file văn bản thường, dùng `CharacterTextSplitter` để chia thành các đoạn có kích thước 1000 ký tự, chồng lấp 50 ký tự.
   - Với file Markdown, dùng `RecursiveCharacterTextSplitter` với cùng kích thước và chồng lấp.

3. **Kết hợp các đoạn:**
   - Các đoạn văn bản từ hai nguồn được kết hợp thành một danh sách chung.

4. **Tạo vector embeddings:**
   - Sử dụng `OpenAIEmbeddings` để chuyển các đoạn văn bản thành vector số.

5. **Xây dựng vectorstore:**
   - Dùng `FAISS` để tạo hệ thống lưu trữ vector, hỗ trợ tìm kiếm hiệu quả.

6. **Tạo retriever:**
   - Chuyển vectorstore thành một retriever với tham số tìm kiếm lấy 4 kết quả phù hợp nhất.

7. **Hàm truy vấn:**
   - `retrieve_knowledge(query: str) -> List[str]` nhận một truy vấn dạng chuỗi, trả về danh sách các đoạn văn bản liên quan dựa trên tìm kiếm vector.

## Mục Đích

Hệ thống này giúp tìm kiếm thông tin hiệu quả trong các tài liệu lớn, có thể áp dụng cho trợ lý ảo, hệ thống hỏi đáp, hoặc phân tích dữ liệu.

## Lưu Ý

- Các thư viện `langchain_community` và `faiss` hỗ trợ xử lý tài liệu, tạo embeddings và tìm kiếm vector.
- Việc chia nhỏ văn bản và tham số chunk size, chunk overlap rất quan trọng để đảm bảo chất lượng tìm kiếm.

---

## Mã Nguồn Chính

```python
from typing import List
from langchain_community.document_loaders import TextLoader, UnstructuredMarkdownLoader  # type:ignore
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings  # type:ignore
from langchain_community.vectorstores import FAISS  # type:ignore

# Tải và chia nhỏ tài liệu văn bản
loader = TextLoader("./docs/reference.txt")
docs = loader.load()
splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# Tải và chia nhỏ tài liệu Markdown
loader = UnstructuredMarkdownLoader("./docs/example_doc.md")
docs_pattem = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
chunks_pattem = splitter.split_documents(docs_pattem)

# Kết hợp các đoạn văn bản
chunks.extend(chunks_pattem)

# Tạo vector embeddings và vectorstore
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# Hàm truy vấn
def retrieve_knowledge(query: str) -> List[str]:
    """Lấy các đoạn văn bản liên quan đến truy vấn."""
    results = retriever.get_relevant_documents(query)
    return [doc.page_content for doc in results]
```

Hy vọng nội dung này giúp bạn hiểu rõ hơn về cách thức hoạt động của mã code và hệ thống tìm kiếm thông tin được xây dựng.