import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

from agent import tag_agent as agent
from tools.retrieve import retrieve_knowledge



if __name__ == "__main__":
    with open("/home/hai/agent2agent/tools/retrieve.py", "r") as f:
        code_sample = f.read()
    f.close()
    # 1. Lấy context
    ctx = retrieve_knowledge("Bạn là một chuyên gia về viết document và trình bảy dạng mardown với từng suy luận logic bám sát tài liệu để do người dùng dễ dàng đọc tài liệu của bạn viết")

    # 2. Gửi prompt
    prompt = (f"""
        Phân tích code sau +{code_sample} , dùng context {ctx} để cải thiện độ chính xác, 
        viết tài liệu dạng markdow theo cú pháp để đọc và lưu file:
    """)
    result = agent.run(prompt)
    print("Kết quả:", result)