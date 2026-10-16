import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

# Import dữ liệu bài kiểm tra
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

# --- Khởi tạo Session State cho cơ sở dữ liệu giả lập trong bộ nhớ ---
if "submissions" not in st.session_state:
    st.session_state.submissions = []  # Lưu danh sách kết quả và lỗi vi phạm

if "cheating_logs" not in st.session_state:
    st.session_state.cheating_logs = []

# --- CSS Tùy chỉnh giao diện chuyên nghiệp & Phát hiện rời màn hình ---
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
    .warning-box {
        background-color: #FEE2E2;
        border: 1px solid #EF4444;
        padding: 10px;
        border-radius: 5px;
        color: #991B1B;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# JavaScript để phát hiện người dùng chuyển tab, thu nhỏ cửa sổ hoặc mất tiêu điểm (blur)
st.markdown("""
    <script>
    document.addEventListener("visibilitychange", function() {
        if (document.hidden) {
            // Gửi tín hiệu cảnh báo qua Streamlit query params hoặc log
            const dataLayer = window.parent.document;
            console.warn("CẢNH BÁO: Học sinh rời khỏi cửa sổ làm bài!");
        }
    });
    </script>
""", unsafe_allow_html=True)


def reset_student_session():
    st.session_state.pop("started", None)
    st.session_state.pop("shuffled_questions", None)
    st.session_state.pop("start_time", None)
    st.session_state.pop("submitted", None)
    st.session_state.pop("score", None)
    st.session_state.pop("violations", None)


# --- THANH ĐIỀU HƯỚNG BÊN TRÁI (SIDEBAR) ---
st.sidebar.title("📌 Điều hướng")
role = st.sidebar.radio("Chọn vai trò:", ["Học sinh làm bài", "Giáo viên quản trị"])

# ==========================================
# KHU VỰC DÀNH CHO HỌC SINH
# ==========================================
if role == "Học sinh làm bài":
    st.markdown(f"<div class='main-title'>{QUIZ_TITLE}</div>", unsafe_allow_html=True)

    # Đăng nhập thông tin học sinh
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
                        # Sao chép câu hỏi để không ảnh hưởng dữ liệu gốc
                        q_copy = q.copy()
                        options = q_copy["options"].copy()
                        correct_answer = options[0]  # Giả định đáp án gốc ở index 0
                        
                        # Xáo trộn đáp án
                        random.shuffle(options)
                        correct_index = options.index(correct_answer)
                        
                        q_copy["options"] = options
                        q_copy["correct_index"] = correct_index
                        shuffled_q.append(q_copy)
                    
                    # Xáo trộn thứ tự câu hỏi
                    random.shuffle(shuffled_q)
                    st.session_state.shuffled_questions = shuffled_q
                    st.rerun()

    else:
        # Kiểm tra nếu học sinh đã nộp bài
        if st.session_state.get("submitted", False):
            st.success("🎉 Bạn đã hoàn thành bài kiểm tra!")
            st.metric("Điểm số của bạn", f"{st.session_state.score} / {len(QUESTIONS)}")
            st.warning(f"Số lần ghi nhận vi phạm (rời tab/thu nhỏ cửa sổ): {st.session_state.violations}")
            
            if st.button("Làm bài kiểm tra mới / Đăng xuất"):
                reset_student_session()
                st.rerun()
        else:
            # Mô phỏng đếm ngược thời gian
            elapsed_time = time.time() - st.session_state.start_time
            remaining_seconds = int(DURATION_MINUTES * 60 - elapsed_time)

            if remaining_seconds <= 0:
                st.warning("⏰ Đã hết thời gian làm bài! Hệ thống đang tự động nộp bài...")
                # Tự động chấm điểm khi hết giờ
                score = 0
                for i, q in enumerate(st.session_state.shuffled_questions):
                    ans = st.session_state.get(f"q_{i}")
                    if ans is not None and ans == q["correct_index"]:
                        score += 1
                st.session_state.score = score
                st.session_state.submitted = True
                
                # Lưu vào bảng điểm chung
                st.session_state.submissions.append({
                    "Học sinh": st.session_state.student_name,
                    "Mã số": st.session_state.student_id,
                    "Điểm số": f"{score}/{len(QUESTIONS)}",
                    "Số lỗi vi phạm": st.session_state.violations,
                    "Thời gian nộp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                st.rerun()

            # Hiển thị đồng hồ đếm ngược và thông tin học sinh
            col1, col2, col3 = st.columns([2, 2, 2])
            with col1:
                st.write(f"👤 **Học sinh:** {st.session_state.student_name} ({st.session_state.student_id})")
            with col2:
                mins, secs = divmod(remaining_seconds, 60)
                st.markdown(f"<div class='timer-box'>⏳ Thời gian còn lại: {mins:02d}:{secs:02d}</div>", unsafe_allow_html=True)
            with col3:
                # Nút ghi nhận vi phạm thủ công hoặc tự động cảnh báo
                if st.button("⚠️ Báo cáo lỗi vi phạm giả lập"):
                    st.session_state.violations += 1
                    st.rerun()
                st.write(f"🚨 Vi phạm ghi nhận: **{st.session_state.violations}** lần")

            st.markdown("---")

            # Form làm bài kiểm tra
            with st.form("quiz_form"):
                student_answers = {}
                for i, q in enumerate(st.session_state.shuffled_questions):
                    st.markdown(f"**Câu {i+1}:** {q['question']}")
                    choice = st.radio(
                        f"Chọn đáp án câu {i+1}:",
                        options=range(len(q["options"])),
                        format_func=lambda x: q["options"][x],
                        key=f"q_{i}",
                        label_visibility="collapsed"
                    )
                    student_answers[i] = choice
                    st.write("")

                submitted_btn = st.form_submit_button("📤 Nộp bài kiểm tra")

                if submitted_btn:
                    score = 0
                    for i, q in enumerate(st.session_state.shuffled_questions):
                        if student_answers.get(i) == q["correct_index"]:
                            score += 1
                    
                    st.session_state.score = score
                    st.session_state.submitted = True
                    
                    # Lưu kết quả vào cơ sở dữ liệu chung
                    st.session_state.submissions.append({
                        "Học sinh": st.session_state.student_name,
                        "Mã số": st.session_state.student_id,
                        "Điểm số": f"{score}/{len(QUESTIONS)}",
                        "Số lỗi vi phạm": st.session_state.violations,
                        "Thời gian nộp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    st.rerun()

            # Tự động làm mới trang mỗi giây để cập nhật đồng hồ đếm ngược
            time.sleep(1)
            st.rerun()


# ==========================================
# KHU VỰC DÀNH CHO GIÁO VIÊN
# ==========================================
elif role == "Giáo viên quản trị":
    st.markdown("<div class='main-title'>🔐 Cổng Quản Trị Giáo Viên</div>", unsafe_allow_html=True)

    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        with st.form("admin_login_form"):
            username = st.text_input("Tài khoản quản trị:")
            password = st.text_input("Mật khẩu:", type="password")
            login_btn = st.form_submit_button("Đăng nhập")

            if login_btn:
                if username == "admin" and password == "Giaovien@2026":
                    st.session_state.admin_logged_in = True
                    st.success("Đăng nhập thành công!")
                    st.rerun()
                else:
                    st.error("Tài khoản hoặc mật khẩu không chính xác!")
    else:
        st.success("Đang đăng nhập với tư cách: Giáo viên (Admin)")
        
        if st.button("Đăng xuất tài khoản quản trị"):
            st.session_state.admin_logged_in = False
            st.rerun()

        st.markdown("---")
        st.subheader("📊 Bảng điểm và Theo dõi lỗi vi phạm của học sinh")

        if len(st.session_state.submissions) == 0:
            st.info("Chưa có học sinh nào nộp bài kiểm tra.")
        else:
            df = pd.DataFrame(st.session_state.submissions)
            st.dataframe(df, use_container_width=True)

            col_a, col_b = st.columns(2)
            with col_a:
                # Chức năng làm mới dữ liệu
                if st.button("🔄 Làm mới dữ liệu bảng điểm"):
                    st.session_state.submissions = []
                    st.success("Đã làm mới dữ liệu thành công!")
                    st.rerun()
            with col_b:
                # Chức năng cho học sinh thi lại (Xóa lịch sử của một học sinh cụ thể)
                student_to_reset = st.selectbox(
                    "Chọn học sinh cho phép thi lại:",
                    options=[s["Học sinh"] + " (" + s["Mã số"] + ")" for s in st.session_state.submissions]
                )
                if st.button("🔄 Cho phép học sinh này thi lại"):
                    name_to_remove = student_to_reset.split(" (")[0]
                    st.session_state.submissions = [
                        s for s in st.session_state.submissions if s["Học sinh"] != name_to_remove
                    ]
                    st.success(f"Đã cho phép học sinh {name_to_remove} thi lại thành công!")
                    st.rerun()
