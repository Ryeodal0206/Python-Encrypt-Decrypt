import os
import base64
import json
import tkinter as tk
from tkinter import filedialog
from ttkbootstrap import ttk, Window
from ttkbootstrap.dialogs import Messagebox
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_file(filepath, password):
    with open(filepath, 'rb') as f:
        data = f.read()
    salt = os.urandom(16)
    key = derive_key(password, salt)
    fernet = Fernet(key)

    metadata = {'filename': os.path.basename(filepath)}
    json_meta = json.dumps(metadata).encode()
    meta_len = len(json_meta).to_bytes(4, 'big')

    encrypted = fernet.encrypt(meta_len + json_meta + data)

    enc_path = filepath + ".enc"
    if os.path.exists(enc_path):
        raise FileExistsError(f"File đã tồn tại: {enc_path}")
    with open(enc_path, 'wb') as f:
        f.write(salt + encrypted)
    return enc_path

def decrypt_file(filepath, password):
    with open(filepath, 'rb') as f:
        file_data = f.read()
    salt = file_data[:16]
    encrypted = file_data[16:]
    key = derive_key(password, salt)
    fernet = Fernet(key)

    try:
        decrypted = fernet.decrypt(encrypted)
        meta_len = int.from_bytes(decrypted[:4], 'big')
        metadata = json.loads(decrypted[4:4 + meta_len])
        filename = metadata['filename']
        out_data = decrypted[4 + meta_len:]
        out_path = os.path.join(os.path.dirname(filepath), f"decrypted_{filename}")
        with open(out_path, 'wb') as f:
            f.write(out_data)
        return out_path
    except Exception:
        raise ValueError("Sai mật khẩu hoặc file hỏng.")

def create_gui():
    app = Window(title="Mã hóa tập tin", themename="litera", size=(450, 390))
    app.place_window_center()
    app.resizable(False, False)

    try:
        app.iconbitmap("app_icon.ico")
    except:
        pass

    file_path_var = tk.StringVar()
    folder_encrypt_path = tk.StringVar()
    folder_decrypt_path = tk.StringVar()

    # Đường dẫn file/thư mục hiển thị
    path_frame = ttk.Frame(app)
    path_frame.pack(anchor="w", padx=50, pady=(10, 0))

    ttk.Label(path_frame, text="📄 Đường dẫn tệp/thư mục đã chọn:", font=("SF UI Display Condensed", 10)).pack(anchor="w")
    path_label = ttk.Entry(path_frame, textvariable=file_path_var, width=35, state="readonly")
    path_label.pack(anchor="w", pady=5)

    # Mật khẩu
    password_frame = ttk.Frame(app)
    password_frame.pack(anchor="w", padx=50, pady=(10, 0))

    ttk.Label(password_frame, text="🔐 Nhập mật khẩu:", font=("SF UI Display Condensed", 10)).pack(anchor="w")
    password_entry = ttk.Entry(password_frame, show="*", width=35)
    password_entry.pack(anchor="w", pady=5)

    def get_password():
        password = password_entry.get()
        if not password:
            Messagebox.show_error("Vui lòng nhập mật khẩu", title="Lỗi")
            return None
        return password

    def choose_encrypt_file():
        path = filedialog.askopenfilename()
        file_path_var.set(path)

    def choose_decrypt_file():
        path = filedialog.askopenfilename(filetypes=[("Encrypted files", "*.enc")])
        file_path_var.set(path)

    def choose_encrypt_folder():
        folder = filedialog.askdirectory()
        folder_encrypt_path.set(folder)
        file_path_var.set(folder)

    def choose_decrypt_folder():
        folder = filedialog.askdirectory()
        folder_decrypt_path.set(folder)
        file_path_var.set(folder)

    def on_ok():
        path = file_path_var.get()
        password = get_password()
        if not path or not password:
            Messagebox.show_error("Vui lòng chọn tệp/thư mục và nhập mật khẩu.")
            return

        if os.path.isfile(path):
            try:
                if path.endswith(".enc"):
                    out = decrypt_file(path, password)
                    Messagebox.show_info(f"Đã giải mã thành công:\n{out}", title="Hoàn tất")
                else:
                    out = encrypt_file(path, password)
                    Messagebox.show_info(f"Đã mã hóa thành công:\n{out}", title="Hoàn tất")

                # Xóa cả đường dẫn và mật khẩu sau khi thành công
                file_path_var.set("")
                password_entry.delete(0, tk.END)

            except ValueError as e:
                # Sai mật khẩu hoặc file hỏng -> chỉ xóa mật khẩu, giữ nguyên đường dẫn
                Messagebox.show_error(str(e))
                password_entry.delete(0, tk.END)

            except FileExistsError as e:
                Messagebox.show_error(str(e))
                file_path_var.set("")
                password_entry.delete(0, tk.END)

            except Exception as e:
                Messagebox.show_error(f"Lỗi khi xử lý file:\n{e}")
                file_path_var.set("")
                password_entry.delete(0, tk.END)

        elif os.path.isdir(path):
            if path == folder_encrypt_path.get():
                files = os.listdir(path)
                count_success = 0
                error_files = []

                for file in files:
                    full_path = os.path.join(path, file)
                    if os.path.isfile(full_path) and not file.endswith(".enc"):
                        try:
                            encrypt_file(full_path, password)
                            count_success += 1
                        except Exception as e:
                            error_files.append(f"{file}: {str(e)}")

                msg = f"Đã mã hóa {count_success} tệp."
                if error_files:
                    msg += "\nMột số file không mã hóa được:\n" + "\n".join(error_files)
                Messagebox.show_info(msg, title="Hoàn tất")

                file_path_var.set("")
                password_entry.delete(0, tk.END)

            elif path == folder_decrypt_path.get():
                files = os.listdir(path)
                count_success = 0
                error_files = []

                for file in files:
                    full_path = os.path.join(path, file)
                    if os.path.isfile(full_path) and file.endswith(".enc"):
                        try:
                            decrypt_file(full_path, password)
                            count_success += 1
                        except ValueError as e:
                            # Sai mật khẩu hoặc file hỏng -> chỉ xóa mật khẩu, giữ nguyên đường dẫn
                            Messagebox.show_error(str(e))
                            password_entry.delete(0, tk.END)
                            return
                        except Exception as e:
                            error_files.append(f"{file}: {str(e)}")

                msg = f"Đã giải mã {count_success} tệp."
                if error_files:
                    msg += "\nMột số file không giải mã được:\n" + "\n".join(error_files)
                Messagebox.show_info(msg, title="Hoàn tất")

                file_path_var.set("")
                password_entry.delete(0, tk.END)

            else:
                Messagebox.show_error("Vui lòng chọn thư mục mã hóa hoặc giải mã đúng.")
                file_path_var.set("")
                password_entry.delete(0, tk.END)

        else:
            Messagebox.show_error("Đường dẫn không hợp lệ hoặc không phải file/thư mục.")
            file_path_var.set("")
            password_entry.delete(0, tk.END)

    button_frame = ttk.Frame(app)
    button_frame.pack(anchor="w", padx=70, pady=5)  # Canh trái + thêm lề
    ttk.Button(button_frame, text="📂 Chọn file để mã hóa", width=30, command=choose_encrypt_file).pack(anchor="w", pady=2)
    ttk.Button(button_frame, text="📥 Chọn file .enc để giải mã", width=30, command=choose_decrypt_file).pack(anchor="w", pady=2)
    ttk.Button(button_frame, text="📁 Chọn thư mục để mã hóa tất cả file", width=30, command=choose_encrypt_folder).pack(anchor="w", pady=2)
    ttk.Button(button_frame, text="📤 Chọn thư mục để giải mã tất cả file .enc", width=30, command=choose_decrypt_folder).pack(anchor="w", pady=2)

    bottom_frame = ttk.Frame(app)
    bottom_frame.pack(fill='x', pady=20, padx=15)
    ttk.Label(bottom_frame, text="Dùng mã hóa AES-256 an toàn", font=('SF UI Display Condensed', 9), foreground="#666").pack(side='left')
    ttk.Button(bottom_frame, text="OK", width=4, command=on_ok, bootstyle="success").pack(side='right')

    app.mainloop()

if __name__ == "__main__":
    create_gui()
