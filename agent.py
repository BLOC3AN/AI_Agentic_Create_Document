from langchain.agents import initialize_agent, Tool
from langchain_community.chat_models import ChatOpenAI #type:ignore
from tools.retrieve import retrieve_knowledge
from tools.analyze import analyze_code
from tools.write import write_doc
from tools.save import save_file

# Khởi tạo LLM
tool_llm = ChatOpenAI(model_name="gpt-4o-mini", top_p=0.85, temperature=0.3)

# Đăng ký tools
tools = [
    Tool(
        name="retrieve_knowledge", 
        func=retrieve_knowledge, 
        description="Lấy kiến thức liên quan từ docs"),
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
        description="Lưu nội dung Markdown tương ứng nhận từ write_doc. Trả về đường dẫn file đã lưu"
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