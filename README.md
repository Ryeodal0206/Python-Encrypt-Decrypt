<p align="center"><img src="https://github.com/Ryeodal0206/Images/blob/main/python.png?raw=true" alt="Python Logo" width="600"</p>
<h1 align="center">Python Encrypt_Decrypt with Password</h1><br><h2 align="center">Mã hóa và giải mã file với AES-256 bảo vệ bằng mật khẩu và xác thực HMAC</h2>

---

## 1. Các thư viện cần cài đặt

- Thư viện bảo mật **AES-256** + **Argon2-CFFI** và GUI **Bootstrap** thay thế cho tkinter mặc định

      pip install ttkbootstrap cryptography argon2-cffi

  
- - Nâng cấp phiên bản
  
        pip install --upgrade ttkbootstrap cryptography argon2-cffi

  
- Thư viện tạo file `.exe`

        pip install pyinstaller

- - Nâng cấp lên phiên bản mới

        pip install --upgrade pyinstaller

---

## 2. Sửa lỗi ***`'python' is not recognized.....`***

- Thêm Python vào hệ thống `PATH` (để gọi Python ở mọi nơi)

- Thêm 2 đường dẫn vào `Environment Variables`

        C:\Users\YTRANG\AppData\Local\Programs\Python\Python313\
    và
        
        C:\Users\YTRANG\AppData\Local\Programs\Python\Python313\Scripts\

- Kiểm tra lại xem đã hoàn thành chưa ***( kiểm tra ở ổ đĩa bất kỳ )***

        python --version

---

## 3. Khởi tạo file `.exe`
>[!NOTE]
>
>- Khi chạy lệnh thì tên tệp `.py` ***không được có dấu cách***

---

- - Không có `icon`

            pyinstaller --noconsole --onefile encrypt_app.py
    
- - Có icon

            pyinstaller --noconsole --onefile --icon=image.ico encrypt_app.py

***hoặc***

 - - Không có `icon`

            pyinstaller --windowed --onefile encrypt_app.py

 - - Có `icon`
 
            pyinstaller --windowed --onefile --icon=app_icon.ico encrypt_app.py
          
---

## 4. Đổi màu nút

- `primary` : ***bootstyle="primary"*** : Xanh lam

- `success` : ***bootstyle="success"*** : Xanh lá
 
- `danger` : ***bootstyle="danger"*** : Đỏ
   
- `warning` : ***bootstyle="warning"*** : Vàng
     
- `info` : ***bootstyle="info"*** : Xanh nhạt

- `secondary` : ***bootstyle="secondary"*** : Xám

- `dark` : ***bootstyle="dark"*** : Đen nhạt
 
- `light` : ***bootstyle="light"*** : Trắng/xám

---

## Khác

<details>
    <summary>Xem thêm</summary>
    
#### 🛠 Lệnh kiểm tra các gói cài đặt

    pip list

#### ⚙ Xóa từng gói thủ công

      pip uninstall "tên gói"

#### ❗ Xóa theo danh sách txt

- Tạo file tên `remove.txt` nhập tên các gói mỗi gói sẽ xuống 1 dòng

      pip uninstall -r remove.txt

#### ✔ Xem các gói đã được gỡ hay chưa

      pip show "tên gói"

---
</details>
