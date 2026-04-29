import google.generativeai as genai
from datetime import datetime
import os # Thêm thư viện hệ thống
from dotenv import load_dotenv # Thêm thư viện đọc file .env

# 1. Tự động load file .env (chỉ có tác dụng khi chạy ở máy Hương)
load_dotenv()

# 2. Lấy API Key từ môi trường (Máy Hương lấy ở .env, Web lấy ở Secrets)
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def ask_ai_finance(user_question, data_context):
    try:
        # Giữ nguyên logic quét model tự động đã chạy tốt của Hương
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_model = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in models else models[0]
        
        model = genai.GenerativeModel(target_model)
        
        # Lấy ngày hiện tại để AI tự điền vào giao dịch nếu Hương không nói ngày
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # PROMPT NÂNG CẤP: Giữ nguyên 100% nội dung của Hương
        prompt = f"""
        Bạn là chuyên gia quản lý tài chính cá nhân của Hương (sinh viên IT).
        Dữ liệu chi tiêu thực tế từ CSV của Hương: {data_context}
        Ngày hôm nay là: {current_date}

        NHIỆM VỤ CỦA BẠN:
        1. PHÂN TÍCH: Dựa vào dữ liệu cũ, hãy xem Hương chi tiêu có hợp lý không? 
           (VD: Nếu thấy Hương ăn kem/trà sữa quá nhiều trong tuần thì phải nhắc nhở).
        2. TƯ VẤN: Trả lời câu hỏi của Hương bằng giọng văn gần gũi, thông minh, đôi khi hơi vui vẻ một chút.
        3. TRÍCH XUẤT (BẮT BUỘC): Nếu câu nói của Hương là một giao dịch mới:
           - Bạn PHẢI trả về dòng này ở CUỐI CÙNG phản hồi:
           ADD_DATA|YYYY-MM-DD|Số tiền|Hạng mục|Ghi chú|Loại
           (Loại chỉ gồm: 'Chi tiêu' hoặc 'Thu nhập'. Số tiền phải là số nguyên dương).

        Câu hỏi của Hương: {user_question}
        Trả lời bằng tiếng Việt:
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Lỗi hệ thống rồi Hương ơi: {str(e)}"