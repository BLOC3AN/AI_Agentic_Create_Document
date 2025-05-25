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

# Phân Tích Mã Code

Mã code này khởi tạo một agent thông minh sử dụng mô hình ngôn ngữ ChatOpenAI và một loạt các công cụ để xử lý kiến thức, phân tích mã, viết tài liệu và lưu file.

## Tổng Quan về Các Thành Phần

### 1. Mô Hình Ngôn Ngữ (tool_llm)

- **Mô tả**: Mô hình ngôn ngữ được sử dụng bởi agent, cụ thể là mô hình GPT-4o-mini. Các tham số `top_p` và `temperature` được điều chỉnh để kiểm soát tính ngẫu nhiên trong phản hồi.

### 2. Danh Sách Các Công Cụ (tools)

- **Mô tả**: Danh sách các công cụ được đăng ký, mỗi công cụ có một chức năng riêng biệt phục vụ cho các hoạt động trong quy trình xử lý.

#### Các Công Cụ Được Sử Dụng

| Tên Công Cụ          | Mục Đích                                                                                       |
|----------------------|------------------------------------------------------------------------------------------------|
| `retrieve_knowledge` | Lấy thông tin từ tài liệu để hỗ trợ trong việc trả lời câu hỏi hoặc cung cấp thông tin bổ sung. |
| `analyze_code`      | Phân tích mã nguồn để hiểu rõ hơn về chức năng và cấu trúc của mã, và chuẩn bị nội dung cho tài liệu. |
| `write_doc`         | Chuyển đổi nội dung phân tích thành định dạng Markdown, giúp cho việc trình bày thông tin trở nên dễ đọc hơn. |
| `save_file`         | Lưu nội dung Markdown vào một file, cho phép người dùng dễ dàng truy cập và chia sẻ tài liệu. |

### 3. Agent

- **Mô tả**: Agent được khởi tạo với khả năng xử lý thông tin một cách tự động và linh hoạt, có khả năng phản hồi với thông tin chi tiết nếu được yêu cầu.

## Các Hàm Chính

Dưới đây là danh sách các hàm chính được sử dụng trong mã:

### 1. `initialize_agent`

- **Mô tả**: Khởi tạo một agent với các công cụ và mô hình ngôn ngữ đã cho.
- **Tham số**:
  - `tools`: Danh sách các công cụ được đăng ký để agent sử dụng.
  - `tool_llm`: Mô hình ngôn ngữ được sử dụng bởi agent.
  - `agent`: Loại agent (ví dụ như 'zero-shot-react-description').
  - `handle_parsing_errors`: Biến boolean cho biết agent có nên xử lý lỗi phân tích hay không.
  - `verbose`: Biến boolean cho biết có nên in thông tin chi tiết ra console hay không.

### 2. `Tool`

- **Mô tả**: Lớp đại diện cho các công cụ mà agent có thể sử dụng.
- **Tham số**:
  - `name`: Tên của công cụ.
  - `func`: Hàm thực hiện chức năng của công cụ.
  - `description`: Mô tả ngắn gọn về công cụ.

### 3. `retrieve_knowledge`

- **Mô tả**: Hàm lấy kiến thức liên quan từ tài liệu.
- **Tham số**: Không có.

### 4. `analyze_code`

- **Mô tả**: Hàm phân tích mã và trả về nội dung dưới dạng markdown chuẩn.
- **Tham số**: Không có.

### 5. `write_doc`

- **Mô tả**: Hàm chuyển đổi phân tích thành định dạng Markdown.
- **Tham số**: Không có.

### 6. `save_file`

- **Mô tả**: Hàm lưu nội dung Markdown vào file và trả về đường dẫn đến file đã lưu.
- **Tham số**: Không có.

## Kết Luận

Mã code này thiết lập một hệ thống có khả năng xử lý và trình bày thông tin một cách hiệu quả thông qua các hàm và công cụ đã được định nghĩa. Điều này giúp người dùng dễ dàng truy cập và hiểu rõ hơn về các khái niệm trong mã.

# Run Code
- Activate VirtualEnviroment 
```bash
source ./agent2agent/bin/activate
```
- Run agent
```bash
python3 main.py
```