import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

# --- KHỞI TẠO AN TOÀN GOOGLE SHEETS (Không làm sập app nếu chưa cấu hình) ---
HAS_GSHEET = False
sheet_client = None

try:
    import gspread
    from google.oauth2.service_account import Credentials
    
    if "gcp_service_account" in st.secrets:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_dict = dict(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        sheet_client = gspread.authorize(creds)
        HAS_GSHEET = True
except Exception as e:
    # Chưa cấu hình secrets hoặc thiếu thư viện sẽ chạy chế độ dự phòng
    HAS_GSHEET = False

def get_sheet():
    if not HAS_GSHEET or sheet_client is None:
        return None
    try:
        sheet_name = st.secrets.get("sheet_name", "KetQuaKiemTraTinHoc6")
        sheet = sheet_client.open(sheet_name).sheet1
        return sheet
    except Exception:
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
            return True
        except Exception:
            return False
    return False

def get_all_submissions_gsheet():
    sheet = get_sheet()
    if sheet:
        try:
            data = sheet.get_all_records()
            if data:
                return pd.DataFrame(data)
        except Exception:
            pass
    return pd.DataFrame(columns=["Học sinh", "Mã số", "Điểm số", "Số lỗi vi phạm", "Thời gian nộp"])

def clear_all_submissions_gsheet():
    sheet = get_sheet()
    if sheet:
        sheet.clear()
        sheet.append_row(["Học sinh", "Mã số", "Điểm số", "Số lỗi vi phạm", "Thời gian nộp"])

def delete_student_submission_gsheet(name, student_id):
    sheet = get_sheet()
    if sheet:
        try:
            cell_list = sheet.findall(str(student_id))
            for cell in cell_list:
                row_values = sheet.row_values(cell.row)
                if len(row_values) > 0 and row_values[0] == str(name):
                    sheet.delete_rows(cell.row)
                    break
        except Exception:
            pass

# --- IMPORT DỮ LIỆU BÀI KIỂM TRA ---
try:
    from quiz_data import QUIZ_TITLE, DURATION_MINUTES, QUESTIONS
except ImportError:
    QUIZ_TITLE = "Bài kiểm tra mặc định"
    DURATION_MINUTES = 10
    QUESTIONS = []

st.set_page_config(
    page_title=QUIZ_TITLE,
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS TÙY CHỈNH GIAO DIỆN ---
st.markdown("""
    <style>
    .main-title {
        font-size: 28px;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 20px;
    }
    .timer-box {
        background-color: #FEF3C7;
        border: 2px solid #F59E0B;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: #B45309;
    }
    </style>
""", unsafe_allow_html=True)

def reset_student_session():
    st.session_state.pop("started", None)
    st.session_state.pop("shuffled_questions", None)
    st.session_state.pop("start_time", None)
    st.session_state.pop("submitted", None)
    st.session_state.pop("score", None)
    st.session_state.pop("violations", None)

# --- THANH ĐIỀU HƯỚNG BÊN TRÁI ---
st.sidebar.title("📌 Điều hướng")
role = st.sidebar.radio("Chọn vai trò:", ["Học sinh làm bài", "Giáo viên quản trị"])

# Hiển thị cảnh báo trạng thái Google Sheets ở sidebar cho giáo viên dễ kiểm tra
if not HAS_GSHEET:
    st.sidebar.warning("⚠️ Chưa kết nối Google Sheets (App chạy chế độ nội bộ).")

# ==========================================
# KHU VỰC DÀNH CHO HỌC SINH
# ==========================================
if role == "Học sinh làm bài":
    st.markdown(f"<div class='main-title'>{QUIZ_TITLE}</div>", unsafe_allow_html=True)

    if "started" not in st.session_state or not st.session_state.started:
        st.info("Vui lòng nhập đầy đủ thông tin bên dưới để bắt đầu làm bài kiểm tra.")
        with st.form("student_info_form"):
            student_name = st.text_input("Họ và tên học sinh:")
            student_id = st.text_input("Mã số học sinh (MSSV):")
            submit_info = st.form_submit_button("Bắt đầu làm bài")

            if submit_info:
                if not student_name.strip() or not student_id.strip():
                    st.error("Vui lòng nhập đầy đủ Họ tên và Mã số học sinh!")
                else:
                    st.session_state.student_name = student_name
                    st.session_state.student_id = student_id
                    st.session_state.started = True
                    st.session_state.violations = 0
                    st.session_state.start_time = time.time()
                    
                    # Xáo trộn câu hỏi và đáp án cho từng học sinh
                    shuffled_q = []
                    for q in QUESTIONS:
                        q_copy = q.copy()
                        options = q_copy["options"].copy()
                        correct_answer = options[0]  # Đáp án gốc ở index 0
                        
                        random.shuffle(options)
                        correct_index = options.index(correct_answer)
                        
                        q_copy["options"] = options
                        q_copy["correct_index"] = correct_index
                        shuffled_q.append(q_copy)
                    
                    random.shuffle(shuffled_q)
                    st.session_state.shuffled_questions = shuffled_q
                    st.rerun()

    else:
        if st.session_state.get("submitted", False):
            st.success("🎉 Bạn đã hoàn thành bài kiểm tra!")
            st.metric("Điểm số của bạn", f"{st.session_state.score} / {len(QUESTIONS)}")
            st.warning(f"Số lần ghi nhận vi phạm (rời tab/thu nhỏ cửa sổ): {st.session_state.violations}")
            
            if st.button("Làm bài kiểm tra mới / Đăng xuất"):
                reset_student_session()
                st.rerun()
        else:
            elapsed_time = time.time() - st.session_state.start_time
            remaining_seconds = int(DURATION_MINUTES * 60 - elapsed_time)

            if remaining_seconds <= 0:
                st.warning("⏰ Đã hết thời gian làm bài! Hệ thống đang tự động nộp bài...")
                score = 0
                for i, q in enumerate(st.session_state.shuffled_questions):
                    ans = st.session_state.get(f"q_{i}")
                    if ans is not None and ans == q["correct_index"]:
                        score += 1
                st.session_state.score = score
                st.session_state.submitted = True
                
                save_submission_gsheet(
                    st.session_state.student_name,
                    st.session_state.student_id,
                    f"{score}/{len(QUESTIONS)}",
                    st.session_state.violations
                )
                st.rerun()

            col1, col2, col3 = st.columns([2, 2, 2])
            with col1:
                st.write(f"👤 **Học sinh:** {st.session_state.student_name} ({st.session_state.student_id})")
            with col2:
                mins, secs = divmod(remaining_seconds, 60)
                st.markdown(f"<div class='timer-box'>⏳ Thời gian còn lại: {mins:02d}:{secs:02d}</div>", unsafe_allow_html=True)
            with col3:
                if st.button("⚠️ Báo cáo lỗi vi phạm giả lập"):
                    st.session_state.violations += 1
                    st.rerun()
                st.write(f"🚨 Vi phạm ghi nhận: **{st.session_state.violations}** lần")

            st.markdown("---")

            with st.form("quiz_form"):
                student_answers = {}
                for i, q in enumerate(st.session_state.shuffled_questions):
                    st.markdown(f"**Câu {i+1}:** {q['question']}")
                    
                    choice = st.radio(
                        f"Chọn đáp án câu {i+1}:",
                        options=range(len(q["options"])),
                        format_func=lambda x: q["options"][x],
                        index=None,
                        key=f"q_{i}",
                        label_visibility="collapsed"
                    )
                    student_answers[i] = choice
                    st.write("")

                submitted_btn = st.form_submit_button("📤 Nộp bài kiểm tra")

                if submitted_btn:
                    score = 0
                    unanswered = 0
                    for i, q in enumerate(st.session_state.shuffled_questions):
                        ans = student_answers.get(i)
                        if ans is None:
                            unanswered += 1
                        elif ans == q["correct_index"]:
                            score += 1
                    
                    if unanswered > 0:
                        st.warning(f"⚠️ Bạn còn {unanswered} câu chưa trả lời. Các câu chưa trả lời tính 0 điểm.")
                    
                    st.session_state.score = score
                    st.session_state.submitted = True
                    
                    save_submission_gsheet(
                        st.session_state.student_name,
                        st.session_state.student_id,
                        f"{score}/{len(QUESTIONS)}",
                        st.session_state.violations
                    )
                    st.rerun()

            time.sleep(1)
            st.rerun()


# ==========================================
# KHU VỰC DÀNH CHO GIÁO VIÊN
# ==========================================
elif role == "Giáo viên quản trị":
    st.markdown("<div class='main-title'>🔐 Cổng Quản Trị Giáo Viên</div>", unsafe_allow_html=True)

    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged
