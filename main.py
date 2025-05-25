import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

from agent import tag_agent as agent
from tools.retrieve import retrieve_knowledge

def run_agent():
    return 

if __name__ == "__main__":
    with open("/home/hai/agent2agent/tools/retrieve.py", "r") as f:
        code_sample = f.read()

    # 1. Lấy context
    ctx = retrieve_knowledge("""Bạn là một chuyên gia về viết document và 
                             trình bày dạng mardown với từng suy luận logic bám sát tài liệu 
                             để do người dùng dễ dàng đọc tài liệu của bạn viết""")

    # 2. Gửi prompt
    prompt = (f"""
        Phân tích code sau ```{code_sample}```, 
        dùng context {ctx} hiểu và cải thiện độ chính xác, 
        viết tài liệu dạng Markdow theo cú pháp để đọc và 
        Khi bạn cần sử dụng một công cụ, bạn PHẢI tạo ra một `Action` và `Action Input`.
        `Action Input` PHẢI là một chuỗi JSON hợp lệ.
        Ví dụ về cách bạn nên gọi công cụ save_file:
            Action: save_file
            Action Input: {{"markdown": "Nội dung tài liệu của tôi...", "file_name": "ten_tai_lieu"}}
        **Luôn kết thúc nhiệm vụ bằng Final Answer và đảm bảo lưu file thành công**
    """)
    result = agent.run(prompt)
    print("Kết quả:", result)