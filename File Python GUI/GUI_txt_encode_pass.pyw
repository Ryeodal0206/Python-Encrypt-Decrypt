import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def encode_text_to_hex(text_path, password):
    # Đọc nội dung của file văn bản
    with open(text_path, 'r') as f:
        text_data = f.read()

    # Mã hóa mật khẩu sử dụng SHA-256
    hashed_password = hashlib.sha256(password.encode()).digest()

    # Kết hợp mật khẩu với dữ liệu văn bản
    text_data_with_password = hashed_password + text_data.encode()

    # Chuyển đổi dữ liệu văn bản kết hợp mật khẩu thành chuỗi hex
    encoded_data = text_data_with_password.hex()

    return encoded_data

def select_text():
    # Hỏi người dùng chọn file văn bản
    text_path = filedialog.askopenfilename(title="Chọn file văn bản", filetypes=[("Text files", "*.txt")])
    if text_path:
        text_path_entry.delete(0, tk.END)
        text_path_entry.insert(0, text_path)

def encode_text():
    # Lấy đường dẫn đến file văn bản và mật khẩu từ người dùng
    text_path = text_path_entry.get()
    password = password_entry.get()

    # Kiểm tra xem người dùng đã nhập đủ thông tin chưa
    if not text_path or not password:
        messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin.")
        return

    try:
        # Mã hóa file văn bản thành chuỗi hex với mật khẩu
        encoded_text_data = encode_text_to_hex(text_path, password)

        # Lấy tên file gốc và thêm đuôi _encoded.txt
        base_name = os.path.basename(text_path)
        file_name, _ = os.path.splitext(base_name)
        save_file_name = f"{file_name}_encoded.txt"

        # Ghi chuỗi hex vào file mới
        with open(save_file_name, 'w') as encoded_file:
            encoded_file.write(encoded_text_data)

        messagebox.showinfo("Thành công", f"File văn bản đã được mã hóa và ghi vào file {save_file_name}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")

# Tạo cửa sổ
root = tk.Tk()
root.title("Mã hóa file văn bản")

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

# Tạo nhãn và ô nhập đường dẫn file văn bản
text_frame = tk.Frame(root, padx=10, pady=5)
text_frame.pack(fill=tk.X)

text_path_label = tk.Label(text_frame, text="File văn bản:", width=10, anchor="w", font=("SF UI Display Condensed", 10, "normal"))
text_path_label.grid(row=0, column=0, sticky="w")

text_path_entry = tk.Entry(text_frame, width=30, font=("SF UI Display Condensed", 12))
text_path_entry.grid(row=0, column=1, padx=(5, 0))

select_text_button = tk.Button(text_frame, height=1, width=8, text="Chọn", command=select_text, font=("SF UI Display Condensed", 10))
select_text_button.grid(row=0, column=2, padx=(5, 0))

# Tạo nhãn và ô nhập mật khẩu
password_frame = tk.Frame(root, padx=10, pady=5)
password_frame.pack(fill=tk.X)

password_label = tk.Label(password_frame, text="Mật khẩu:", width=10, anchor="w", font=("SF UI Display Condensed", 10, "normal"))
password_label.grid(row=0, column=0, sticky="w")

password_entry = tk.Entry(password_frame, show="*", width=30, font=("SF UI Display Condensed", 12))
password_entry.grid(row=0, column=1, padx=(5, 0))

# Tạo nút mã hóa
encode_button = tk.Button(root, width=10, text="Mã hóa", command=encode_text, font=("SF UI Display Condensed", 10, "bold"))
encode_button.pack(pady=10)

# Thêm đoạn văn bản tùy chỉnh
info_label = tk.Label(root, text="Code được phát triển bởi Lê Đạt ❤", font=("SF UI Display Condensed", 10))
info_label.pack(side=tk.LEFT) #, pady=5)

# Chạy ứng dụng
root.mainloop()
