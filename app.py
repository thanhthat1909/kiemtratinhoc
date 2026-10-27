import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# --- KẾT NỐI GOOGLE SHEETS (Đã bật hiển thị lỗi chi tiết) ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

@st.cache_resource
def get_gspread_client():
    try:
        creds_dict = dict(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error(f"❌ Lỗi xác thực Google Secrets: {e}")
        return None

def get_sheet():
    client = get_gspread_client()
    if client is None:
        return None
    sheet_name = st.secrets.get("sheet_name", "KetQuaKiemTraTinHoc6")
    try:
        # Mở file Google Sheets có sẵn
        sheet = client.open(sheet_name).sheet1
        return sheet
    except Exception as e:
        st.error(f"❌ Không tìm thấy file Google Sheets '{sheet_name}': {e}. Hãy chắc chắn đã tạo file và chia sẻ quyền Editor cho Service Account!")
        return None

def save_submission_gsheet(name, student_id, score, violations):
    sheet = get_sheet()
    if sheet:
        try:
            sheet.append_row([
                str(name),
                str(student_id),
                str(score),
                int(violations),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ])
            st.success("✅ Đã lưu kết quả thành công lên Google Sheets!")
        except Exception as e:
            st.error(f"❌ Lỗi khi ghi dữ liệu vào dòng: {e}")
    else:
        st.error("❌ Không thể kết nối tới Google Sheets để lưu điểm!")

def get_all_submissions_gsheet():
    sheet = get_sheet()
    if sheet:
        try:
            data = sheet.get_all_records()
            if data:
                return pd.DataFrame(data)
        except Exception as e:
            st.error(f"❌ Lỗi đọc dữ liệu từ Google Sheets: {e}")
    return pd.DataFrame(columns=["Học sinh", "Mã số", "Điểm số", "Số lỗi vi phạm", "Thời gian nộp"])

def clear_all_submissions_gsheet():
    sheet = get_sheet()
    if sheet:
        sheet.clear()
        sheet.append_row(["Học sinh", "Mã số", "Điểm số", "Số lỗi vi phạm", "Thời gian nộp"])

def delete_student_submission_gsheet(name, student_id):
    sheet = get_sheet()
    if sheet:
        cell_list = sheet.findall(str(student_id))
        for cell in cell_list:
            row_values = sheet.row_values(cell.row)
            if len(row_values) > 0 and row_values[0] == str(name):
                sheet.delete_rows(cell.row)
                break
