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
    with open("/home/hai/agent2agent/docs/example_doc.md", "r") as f:
        pattem_doc = f.read()
    f.close()


    # 1. Lấy context
    ctx = retrieve_knowledge("Bạn là một chuyên gia về viết document dạng mardown với từng suy luận logic để do người dùng dễ dàng đọc tài liệu củas bạn viết")

    # 2. Gửi prompt
    prompt = (f"""
        Phân tích code sau , dùng context {ctx} để cải thiện độ chính xác, 
        viết tài liệu dạng markdow tham khảo {pattem_doc} để đọc và lưu file:+{code_sample}
    """)
    result = agent.run(prompt)
    print("Kết quả:", result)