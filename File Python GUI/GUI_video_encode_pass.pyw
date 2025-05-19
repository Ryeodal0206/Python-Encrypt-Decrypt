import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def encode_video_to_hex(video_path, password):
    # Đọc nội dung của video dưới dạng byte
    with open(video_path, 'rb') as f:
        video_data = f.read()

    # Mã hóa mật khẩu sử dụng SHA-256
    hashed_password = hashlib.sha256(password.encode()).digest()

    # Kết hợp mật khẩu với dữ liệu video
    video_data_with_password = hashed_password + video_data

    # Chuyển đổi dữ liệu video kết hợp mật khẩu thành chuỗi hex
    encoded_data = video_data_with_password.hex()

    return encoded_data

def select_video():
    # Hỏi người dùng chọn video
    video_path = filedialog.askopenfilename(title="Chọn video", filetypes=[("Video files", "*.mp4;*.avi")])
    if video_path:
        video_path_entry.delete(0, tk.END)
        video_path_entry.insert(0, video_path)

def encode_video():
    # Lấy đường dẫn đến video và mật khẩu từ người dùng
    video_path = video_path_entry.get()
    password = password_entry.get()

    # Kiểm tra xem người dùng đã nhập đủ thông tin chưa
    if not video_path or not password:
        messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
        return

    try:
        # Mã hóa video thành chuỗi hex với mật khẩu
        encoded_video_data = encode_video_to_hex(video_path, password)

        # Lấy tên file gốc và thêm đuôi .txt
        base_name = os.path.basename(video_path)
        file_name, _ = os.path.splitext(base_name)
        encoded_file_name = f"{file_name}.txt"

        # Ghi chuỗi hex vào file mới
        with open(encoded_file_name, 'w') as encoded_file:
            encoded_file.write(encoded_video_data)

        messagebox.showinfo("Thành công", f"Video đã được mã hóa và ghi vào file {encoded_file_name}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")

# Tạo cửa sổ
root = tk.Tk()
root.title("Mã hóa video")

# Khoảng trống trên cùng của GUI
top_spacing_frame = tk.Frame(root, height=30)
top_spacing_frame.pack()

# Tính toán kích thước và vị trí của cửa sổ
window_width = 600
window_height = 200

# Khóa kích thước GUI
root.resizable(False, False)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Tạo nhãn và ô nhập đường dẫn video
video_frame = tk.Frame(root, padx=10, pady=5)
video_frame.pack(fill=tk.X)

video_path_label = tk.Label(video_frame, text="Video:", width=10, anchor="w", font=("SF UI Display Condensed", 10, "normal"))
video_path_label.grid(row=0, column=0, sticky="w")

video_path_entry = tk.Entry(video_frame, width=30, font=("SF UI Display Condensed", 12))
video_path_entry.grid(row=0, column=1, padx=(5, 0))

select_video_button = tk.Button(video_frame, height=1, width=8, text="Chọn", command=select_video, font=("SF UI Display Condensed", 10))
select_video_button.grid(row=0, column=2, padx=(5, 0))

# Tạo nhãn và ô nhập mật khẩu
password_frame = tk.Frame(root, padx=10, pady=5)
password_frame.pack(fill=tk.X)

password_label = tk.Label(password_frame, text="Mật khẩu:", width=10, anchor="w", font=("SF UI Display Condensed", 10, "normal"))
password_label.grid(row=0, column=0, sticky="w")

password_entry = tk.Entry(password_frame, show="*", width=30, font=("SF UI Display Condensed", 12))
password_entry.grid(row=0, column=1, padx=(5, 0))

# Tạo nút mã hóa
encode_button = tk.Button(root, width=10, text="Mã hóa", command=encode_video, font=("SF UI Display Condensed", 10, "bold"))
encode_button.pack(pady=10)

# Thêm đoạn văn bản tùy chỉnh
info_label = tk.Label(root, text="Code được phát triển bởi Lê Đạt ❤", font=("SF UI Display Condensed", 10))
info_label.pack(side=tk.LEFT) #, pady=5)

# Chạy ứng dụng
root.mainloop()
