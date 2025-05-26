from langchain.agents import initialize_agent, Tool
from langchain_community.chat_models import ChatOpenAI #type:ignore
from tools.retrieve import RetriveKnowledge  #retrieve_knowledge
from tools.analyze import analyze_code
from tools.write import write_doc
from tools.save import save_file
from functools import partial

# Khởi tạo LLM
tool_llm = ChatOpenAI(model_name="gpt-4.1-mini", top_p=0.85, temperature=0.3)
# Gói hàm write_doc với LLM đã có sẵn


# Đăng ký tools
tools = [
    Tool(
        name="retrieve_knowledge", 
        func=RetriveKnowledge().retrieve_knowledge,#retrieve_knowledge, 
        description="Lấy kiến thức liên quan từ các nguồn tham khảo"),
    Tool(
        name="analyze_code", 
        func=analyze_code, 
        description="Phân tích code và trả về nội dung dạng markdown chuẩn"),
    Tool(
        name="write_doc", 
        func=write_doc, 
        description="Chuyển analysis thành Markdown. Trả về nội dung Markdown đã viết"),
    Tool(
        name="save_file",
        func=save_file,
        description="""Lưu nội dung dạng Markdown vào một tệp.
        Công cụ này yêu cầu 2 đối số:
        1. 'markdown': Nội dung tài liệu dưới dạng chuỗi Markdown cần lưu.
        2. 'file_name': Tên của tệp mà bạn muốn lưu tài liệu vào (không cần thêm đuôi .md, công cụ sẽ tự thêm).ví dụ summary_document
        Hãy sử dụng công cụ này khi bạn đã hoàn thành việc tạo tài liệu Markdown và muốn lưu nó lại.
        ví dụ: save_file(markdown = #... , file_name='summary_code')
        """,
),
]

# Tạo agent
tag_agent = initialize_agent(
    tools,
    tool_llm,
    agent="zero-shot-react-description",
    handle_parsing_errors=True,
    verbose=True
)