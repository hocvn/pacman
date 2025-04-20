## Project Planning and Task Assignment

Each member was assigned specific tasks, and all members achieved full task completion.

| MSSV     | Name              | Assigned Task                                                               | Completion |
| -------- | ----------------- | --------------------------------------------------------------------------- | ---------- |
| 22120050 | Hồ Mạnh Đào       | UCS implementation, Update README file                                      | 100%       |
| 22120113 | Nguyễn Việt Hoàng | BFS implementation, Game Menu, Scoring, Time & Memory Analysis              | 100%       |
| 22120115 | Đỗ Thái Học       | DFS implementation, Game UI, Time & Memory Analysis, Video Recording        | 100%       |
| 22120418 | Huỳnh Trần Ty     | A\* implementation, Time & Memory Analysis, Graphs and Final Report Writing | 100%       |

---

# Hướng Dẫn Chạy Chương Trình Pacman

## Yêu Cầu Hệ Thống

- Python 3.10 trở lên
- Thư viện `pygame`
- Các thư viện chuẩn: `heapq`, `deque`, `tracemalloc`, `time`, v.v.

### Cài Đặt Thư Viện

Chạy lệnh sau trong terminal để cài đặt tất cả thư viện:

```bash
pip install -r requirements.txt
```

---

## Cách Chạy Chương Trình

### Bước 1: Tải mã nguồn

Clone từ GitHub hoặc tải về máy:

```bash
git clone https://github.com/hocvn/pacman.git
cd pacman
```

### Bước 2: Chạy chương trình

Chạy file chính của game:

```bash
python main.py
```

---

## Cách Chơi

- Khi khởi động, trò chơi sẽ tự hiển thị cửa sổ.
- Mỗi con ma sử dụng một thuật toán tìm đường khác nhau (DFS, BFS, UCS, A\*).
- Pacman di chuyển ngẫu nhiên hoặc theo lập trình.
- Quan sát hành vi di chuyển và kết quả tìm kiếm được in ra **console**:
  - Thời gian tìm kiếm
  - Dung lượng bộ nhớ sử dụng
  - Số lượng nút mở rộng

---

## Ghi Chú Thêm

- Bạn có thể chỉnh sửa vị trí bắt đầu của ghost và pacman trong code để thực hiện các thí nghiệm khác nhau.
- Nếu muốn kiểm tra riêng từng thuật toán, chỉnh sửa phần gọi hàm tương ứng trong `main.py`.

---

_Đây là hướng dẫn cơ bản để chạy và kiểm thử chương trình Pacman sử dụng AI thuật toán tìm đường._
