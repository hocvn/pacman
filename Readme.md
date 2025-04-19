
#  Hướng Dẫn Chạy Chương Trình Pacman

##  Yêu Cầu Hệ Thống

- Python 3.10 trở lên
- Thư viện `pygame`
- Các thư viện chuẩn: `heapq`, `deque`, `tracemalloc`, `time`, v.v.

###  Cài Đặt Thư Viện

Mở terminal (hoặc CMD) và chạy lệnh sau để cài đặt pygame:

```bash
pip install pygame
```

---

##  Cách Chạy Chương Trình

### Bước 1: Tải mã nguồn

Clone từ GitHub hoặc tải về máy:

```bash
git clone https://github.com/your-username/pacman-ai.git
cd pacman-ai
```

*(Thay link bằng link repo của bạn nếu có)*

### Bước 2: Chạy chương trình

Chạy file chính của game:

```bash
python pacman.py
```

---

## Cách Chơi

- Khi khởi động, trò chơi sẽ tự hiển thị cửa sổ.
- Mỗi con ma sử dụng một thuật toán tìm đường khác nhau (DFS, BFS, UCS, A*).
- Pacman di chuyển ngẫu nhiên hoặc theo lập trình.
- Quan sát hành vi di chuyển và kết quả tìm kiếm được in ra **console**:  
  -  Thời gian tìm kiếm  
  -  Dung lượng bộ nhớ sử dụng  
  -  Số lượng nút mở rộng

---

##  Ghi Chú Thêm

- Bạn có thể chỉnh sửa vị trí bắt đầu của ghost và pacman trong code để thực hiện các thí nghiệm khác nhau.
- Nếu muốn kiểm tra riêng từng thuật toán, chỉnh sửa phần gọi hàm tương ứng trong `pacman.py`.

---

 *Đây là hướng dẫn cơ bản để chạy và kiểm thử chương trình Pacman sử dụng AI thuật toán tìm đường.*
