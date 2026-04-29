import streamlit as st
import pandas as pd
import plotly.express as px
from modules.ai_agent import ask_ai_finance
import os

st.set_page_config(layout="wide", page_title="AI Finance - 69IT1")

# 1. ĐỌC DỮ LIỆU (Giữ nguyên logic của Hương)
file_path = 'data/sample_data.csv'
df = pd.DataFrame(columns=['date', 'amount', 'category', 'note', 'type'])

if os.path.exists(file_path):
    try:
        temp_df = pd.read_csv(file_path)
        if not temp_df.empty:
            temp_df['date'] = pd.to_datetime(temp_df['date'])
            df = temp_df.sort_values(by='date')
    except Exception as e:
        st.error(f"Lỗi đọc file: {e}")

st.title("💰 Quản lý Tài chính - 69IT1")

# 2. HIỂN THỊ BIỂU ĐỒ & BẢNG (Giữ nguyên 100% giao diện của Hương)
if not df.empty:
    df_exp = df[df['type'] == 'Chi tiêu']
    if not df_exp.empty:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(px.pie(df_exp, values='amount', names='category', title='Tỷ trọng chi tiêu'), use_container_width=True)
        with c2:
            daily = df_exp.groupby('date')['amount'].sum().reset_index()
            st.plotly_chart(px.line(daily, x='date', y='amount', title='Xu hướng chi tiêu'), use_container_width=True)
    
    st.subheader("📋 Nhật ký giao dịch")
    st.dataframe(df.sort_values(by='date', ascending=False), use_container_width=True)
else:
    st.info("Chưa có dữ liệu. Hãy nhập giao dịch để bắt đầu!")

st.write("---")

# 3. PHẦN AI (Gia cố phần lưu file để tránh dính dòng)
user_input = st.text_input("Nhập câu hỏi (VD: Ăn kem 25000):")

if user_input:
    with st.spinner('Đang kết nối với trí tuệ nhân tạo...'):
        ai_res = ask_ai_finance(user_input, str(df.to_dict())) 
    
    if "429" in str(ai_res) or "quota" in str(ai_res).lower():
        st.error("⚠️ Hệ thống đang quá tải lượt yêu cầu. Hương đợi khoảng 1 phút rồi thử lại nhé!")
    else:
        st.info(ai_res)
        
        if "ADD_DATA|" in ai_res:
            try:
                p = ai_res.split("ADD_DATA|")[1].split("|")
                new_row = pd.DataFrame([{
                    'date': p[0].strip(),
                    'amount': int(p[1].strip()),
                    'category': p[2].strip(),
                    'note': p[3].strip(),
                    'type': p[4].strip()
                }])
                
                # --- PHẦN FIX LỖI DÍNH DÒNG ---
                # Mở file kiểm tra và ép xuống dòng mới trước khi ghi tiếp
                with open(file_path, "a", encoding="utf-8") as f:
                    # Kiểm tra xem file có rỗng không, nếu không rỗng thì mới kiểm tra xuống dòng
                    if os.path.getsize(file_path) > 0:
                        # Đảm bảo có một dấu xuống dòng trước khi ghi dữ liệu mới
                        f.write("\n")
                
                # Sau khi đã đảm bảo có dòng mới, tiến hành lưu dữ liệu
                new_row.to_csv(file_path, mode='a', header=False, index=False, encoding='utf-8')
                # ------------------------------
                
                st.success("✅ Đã lưu giao dịch vào dòng riêng biệt!")
                st.rerun() 
            except Exception as e:
                st.warning(f"Lỗi khi lưu dữ liệu: {e}. Hương đóng file Excel chưa?")