import google.generativeai as genai
from datetime import datetime
import os
from dotenv import load_dotenv
import time

# Load env
load_dotenv()

# API key
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# ✅ FIX 1: Hardcode model (tránh gọi list_models mỗi lần)
MODEL_NAME = "gemini-1.5-flash"
model = genai.GenerativeModel(MODEL_NAME)

def ask_ai_finance(user_question, data_context):
    try:
        if not api_key:
            return "Thiếu API key rồi!"

        current_date = datetime.now().strftime("%Y-%m-%d")

        prompt = f"""
        Bạn là chuyên gia quản lý tài chính cá nhân của Hương (sinh viên IT).
        Dữ liệu chi tiêu thực tế từ CSV của Hương: {data_context}
        Ngày hôm nay là: {current_date}

        NHIỆM VỤ CỦA BẠN:
        1. PHÂN TÍCH: Dựa vào dữ liệu cũ, hãy xem Hương chi tiêu có hợp lý không? 
        2. TƯ VẤN: Trả lời câu hỏi của Hương bằng giọng văn gần gũi, thông minh.
        3. TRÍCH XUẤT (BẮT BUỘC): Nếu là giao dịch mới:
           ADD_DATA|YYYY-MM-DD|Số tiền|Hạng mục|Ghi chú|Loại

        Câu hỏi của Hương: {user_question}
        Trả lời bằng tiếng Việt:
        """

        # ✅ FIX 2: Retry khi bị 429
        for i in range(3):
            try:
                response = model.generate_content(prompt)
                return response.text
            except Exception as e:
                if "429" in str(e):
                    time.sleep(2)  # đợi rồi thử lại
                else:
                    raise e

        return "Server đang bận, thử lại sau vài giây nhé!"

    except Exception as e:
        print("DEBUG ERROR:", e)  # log ra để debug
        return f"Lỗi hệ thống rồi Hương ơi: {str(e)}"