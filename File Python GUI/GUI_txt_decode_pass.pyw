import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def decode_hex_to_text(encoded_text_data, password):
    # Chuyển đổi chuỗi hex thành dữ liệu văn bản kết hợp mật khẩu
    text_data_with_password = bytes.fromhex(encoded_text_data)

    # Tách mật khẩu và dữ liệu đã mã hóa từ dữ liệu văn bản
    hashed_password = text_data_with_password[:32]
    encrypted_data = text_data_with_password[32:]

    # Mã hóa mật khẩu sử dụng SHA-256
    input_password_hash = hashlib.sha256(password.encode()).digest()

    # So sánh mật khẩu đã nhập với mật khẩu đã mã hóa trong dữ liệu văn bản
    if hashed_password != input_password_hash:
        messagebox.showerror("Lỗi", "Mật khẩu không đúng.")
        password_entry.delete(0, tk.END)  # Xóa nội dung hiện tại của ô nhập mật khẩu
        return None

    # Giải mã dữ liệu văn bản
    return encrypted_data.decode()

def select_file():
    file_path = filedialog.askopenfilename(title="Chọn file đã mã hóa", filetypes=[("Text files", "*.txt")])
    if file_path:
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(0, file_path)

def decrypt_text():
    file_path = file_path_entry.get()
    if not file_path:
        messagebox.showerror("Lỗi", "Vui lòng chọn file đã mã hóa.")
        return

    with open(file_path, 'r') as encoded_file:
        encoded_text_data = encoded_file.read().strip()

    password_input = password_entry.get()
    decoded_text_data = decode_hex_to_text(encoded_text_data, password_input)

    if decoded_text_data:
        # Lấy tên file gốc và thêm đuôi _decoded.txt
        base_name = os.path.basename(file_path)
        file_name, _ = os.path.splitext(base_name)
        
        if file_name.endswith("_encoded"):
            file_name = file_name[:-8]  # Xóa bỏ "_encoded" khỏi tên file
        save_file_name = f"{file_name}_decoded.txt"

        save_path = filedialog.asksaveasfilename(initialfile=save_file_name, defaultextension=".txt", filetypes=[("Text files", "*.txt")], title="Lưu file đã giải mã")
        if save_path:
            with open(save_path, 'w') as decoded_file:
                decoded_file.write(decoded_text_data)
                messagebox.showinfo("Thành công", f"Dữ liệu đã được giải mã và lưu vào file {save_path}.")
                file_path_entry.delete(0, tk.END) # Xóa nội dung hiện tại của ô nhập file mã hóa
                password_entry.delete(0, tk.END) # Xóa nội dung hiện tại của ô nhập mật khẩu

# Tạo cửa sổ
root = tk.Tk()
root.title("Giải mã file văn bản")

# Khoảng trống trên cùng của GUI
top_spacing_frame = tk.Frame(root, height=30)
top_spacing_frame.pack()

# Tính toán vị trí để cửa sổ xuất hiện giữa màn hình
window_width = 600
window_height = 200

# Khóa kích thước GUI
root.resizable(False, False)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Tạo nhãn và ô nhập đường dẫn file đã mã hóa
file_frame = tk.Frame(root, padx=10, pady=5)
file_frame.pack(fill=tk.X)

file_path_label = tk.Label(file_frame, text="File đã mã hóa:", width=15, anchor="w", font=("SF UI Display Condensed", 10, "normal"))
file_path_label.grid(row=0, column=0, sticky="w")

file_path_entry = tk.Entry(file_frame, width=30, font=("SF UI Display Condensed", 12))
file_path_entry.grid(row=0, column=1, padx=(5, 0))

select_file_button = tk.Button(file_frame, height=1, width=8, text="Thêm", command=select_file, font=("SF UI Display Condensed", 10))
select_file_button.grid(row=0, column=2, padx=(5, 0))

# Tạo nhãn và ô nhập mật khẩu
password_frame = tk.Frame(root, padx=10, pady=5)
password_frame.pack(fill=tk.X)

password_label = tk.Label(password_frame, text="Mật khẩu giải mã:", width=15, anchor="w", font=("SF UI Display Condensed", 10, "normal"))
password_label.grid(row=0, column=0, sticky="w")

password_entry = tk.Entry(password_frame, show="", width=30, font=("SF UI Display Condensed", 12))
password_entry.grid(row=0, column=1, padx=(5, 0))

# Tạo nút giải mã
decrypt_button = tk.Button(root, width=10, text="Giải mã", command=decrypt_text, font=("SF UI Display Condensed", 10, "bold"))
decrypt_button.pack(pady=10)

# Thêm đoạn văn bản tùy chỉnh
info_label = tk.Label(root, text="Code được phát triển bởi Lê Đạt ❤", font=("SF UI Display Condensed", 10))
info_label.pack(side=tk.LEFT) #, pady=5)

# Chạy ứng dụng
root.mainloop()
