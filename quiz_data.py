# quiz_data.py

QUIZ_TITLE = "Kiểm tra Môn Tin Học - Lớp 6 (Bài 1 đến Bài 4)"
DURATION_MINUTES = 15  # Thời gian làm bài (phút)

# Danh sách câu hỏi bám sát SGK Kết nối tri thức và cuộc sống
# (Đáp án đúng luôn nằm ở vị trí đầu tiên index 0, code sẽ tự động xáo trộn)
QUESTIONS = [
    {
        "id": 1,
        "question": "Theo quan điểm khoa học máy tính, thông tin là gì?",
        "options": [
            "Tất cả những gì đem lại hiểu biết về thế giới xung quanh và về chính con người.",
            "Chỉ là các con số và văn bản được in trên sách báo.",
            "Những tin tức chỉ có trên tivi và mạng internet.",
            "Những lời nói giao tiếp hàng ngày giữa con người với nhau."
        ]
    },
    {
        "id": 2,
        "question": "Dạng thông tin nào dưới đây bao gồm các hình vẽ hoặc bức ảnh?",
        "options": [
            "Dạng hình ảnh",
            "Dạng văn bản",
            "Dạng âm thanh",
            "Dạng số liệu"
        ]
    },
    {
        "id": 3,
        "question": "Con người thu nhận thông tin thị giác chủ yếu thông qua cơ quan nào?",
        "options": [
            "Mắt",
            "Tai",
            "Mũi",
            "Da"
        ]
    },
    {
        "id": 4,
        "question": "Tiếng chim hót hay tiếng đàn phát ra thuộc dạng thông tin nào?",
        "options": [
            "Dạng âm thanh",
            "Dạng văn bản",
            "Dạng hình ảnh",
            "Dạng chữ viết"
        ]
    },
    {
        "id": 5,
        "question": "Bản tin dự báo thời tiết kết hợp những dạng thông tin cơ bản nào?",
        "options": [
            "Văn bản, hình ảnh và âm thanh",
            "Chỉ có văn bản và số liệu",
            "Chỉ có âm thanh và hình ảnh tĩnh",
            "Chỉ có văn bản và âm thanh"
        ]
    },
    {
        "id": 6,
        "question": "Đâu là vật mang tin giúp con người lưu trữ thông tin lâu dài qua nhiều thế hệ?",
        "options": [
            "Sách, vở, bia đá, ổ cứng máy tính",
            "Lời nói truyền miệng trực tiếp",
            "Tiếng động trong tự nhiên",
            "Ánh sáng mặt trời ban ngày"
        ]
    },
    {
        "id": 7,
        "question": "Hoạt động nào dưới đây thể hiện việc trao đổi thông tin?",
        "options": [
            "Em gửi thư điện tử (email) cho bạn để hỏi bài tập",
            "Em cất quyển sách vở vào trong cặp",
            "Em ghi nhớ công thức toán học vào đầu",
            "Em quan sát bông hoa hồng trong vườn"
        ]
    },
    {
        "id": 8,
        "question": "Thiết bị nào sau đây dùng để lưu trữ dữ liệu số trong máy tính?",
        "options": [
            "Ổ cứng (Hard Drive), USB, thẻ nhớ",
            "Chuột máy tính và bàn phím",
            "Màn hình và loa máy tính",
            "Máy in và máy quét"
        ]
    },
    {
        "id": 9,
        "question": "Ưu điểm nổi bật của việc lưu trữ thông tin bằng thiết bị số so với sách vở truyền thống là gì?",
        "options": [
            "Lưu trữ được dung lượng rất lớn, dễ dàng tìm kiếm và sao chép",
            "Không bao giờ bị hỏng hay mất dữ liệu dù thế nào",
            "Không cần sử dụng điện năng khi đọc",
            "Có thể cầm nắm và ngửi trực tiếp bằng tay"
        ]
    },
    {
        "id": 10,
        "question": "Việc trao đổi thông tin đóng vai trò gì trong đời sống con người?",
        "options": [
            "Giúp con người truyền đạt hiểu biết, kinh nghiệm và kết nối với nhau",
            "Chỉ để giải trí sau giờ học căng thẳng",
            "Giúp làm giảm trọng lượng của não bộ",
            "Làm cho máy tính chạy nhanh hơn"
        ]
    },
    {
        "id": 11,
        "question": "Máy tính giúp ích gì cho ngành giáo dục và việc học tập của học sinh?",
        "options": [
            "Cung cấp kho tư liệu phong phú, học trực tuyến và làm bài tập",
            "Thay thế hoàn toàn giáo viên đứng lớp",
            "Giúp học sinh không cần phải suy nghĩ khi làm bài",
            "Giúp học sinh viết chữ đẹp hơn trên giấy"
        ]
    },
    {
        "id": 12,
        "question": "Trong lĩnh vực y tế, máy tính được ứng dụng để làm gì?",
        "options": [
            "Quản lý bệnh án, hỗ trợ chụp X-quang, cộng hưởng từ và phẫu thuật robot",
            "Trồng cây dược liệu tự động ngoài ruộng",
            "Dự báo thời tiết nắng mưa hằng ngày",
            "Thiết kế thời trang cho bác sĩ"
        ]
    },
    {
        "id": 13,
        "question": "Phát biểu nào sau đây nói đúng về vai trò của máy tính trong cuộc sống hiện đại?",
        "options": [
            "Máy tính là công cụ hỗ trợ đắc lực, không thể thiếu trong nhiều lĩnh vực",
            "Máy tính chỉ dùng để chơi trò chơi điện tử giải trí",
            "Máy tính chỉ phục vụ cho các nhà khoa học vũ trụ",
            "Máy tính hoàn toàn thay thế con người trong mọi việc"
        ]
    },
    {
        "id": 14,
        "question": "Nhờ có máy tính và mạng Internet, hoạt động mua sắm của con người trở nên thuận lợi hơn qua hình thức nào?",
        "options": [
            "Thương mại điện tử (mua sắm trực tuyến)",
            "Đến trực tiếp chợ truyền thống vào nửa đêm",
            "Viết thư tay gửi cho cửa hàng",
            "Gọi điện thoại bàn truyền thống"
        ]
    },
    {
        "id": 15,
        "question": "Robot thông minh (được điều khiển bằng máy tính) thường được ứng dụng trong các công việc gì?",
        "options": [
            "Công việc nguy hiểm, lặp đi lặp lại hoặc ở môi trường độc hại",
            "Đi học thay cho học sinh tiểu học",
            "Trò chuyện tâm sự thay cho bạn bè",
            "Thay thế con người ăn uống hàng ngày"
        ]
    },
    {
        "id": 16,
        "question": "Mô hình xử lý thông tin 3 bước của máy tính gồm những giai đoạn nào theo đúng thứ tự?",
        "options": [
            "Nhận thông tin (Input) -> Xử lý thông tin -> Đưa ra kết quả (Output)",
            "Đưa ra kết quả -> Xử lý thông tin -> Nhận thông tin",
            "Xử lý thông tin -> Nhận thông tin -> Đưa ra kết quả",
            "Lưu trữ dữ liệu -> Nhập văn bản -> In ra giấy"
        ]
    },
    {
        "id": 17,
        "question": "Bộ phận nào của máy tính thực hiện chức năng chính là 'Xử lý thông tin'?",
        "options": [
            "Bộ xử lý trung tâm (CPU)",
            "Bàn phím và chuột",
            "Màn hình và loa",
            "Máy in"
        ]
    },
    {
        "id": 18,
        "question": "Thiết bị nào sau đây đóng vai trò là thiết bị đưa thông tin vào (Input)?",
        "options": [
            "Bàn phím, chuột, máy quét (scanner)",
            "Màn hình, máy in, loa",
            "Ổ cứng, USB, thẻ nhớ",
            "Quạt tản nhiệt của máy tính"
        ]
    },
    {
        "id": 19,
        "question": "Thiết bị nào dưới đây là thiết bị đưa thông tin ra (Output)?",
        "options": [
            "Màn hình và máy in",
            "Bàn phím và chuột",
            "Máy quét mã vạch",
            "Micro thu âm"
        ]
    },
    {
        "id": 20,
        "question": "Thành phần của một hệ thống máy tính nói chung bao gồm những nhóm nào chính?",
        "options": [
            "Phần cứng (Hardware) và phần mềm (Software)",
            "Màn hình và bàn phím",
            "Dây cáp điện và nguồn điện",
            "Hệ điều hành và trò chơi điện tử"
        ]
    }
]
