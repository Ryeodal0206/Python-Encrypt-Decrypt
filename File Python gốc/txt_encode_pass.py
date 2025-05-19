import hashlib

def encode_text_to_hex(text_path, password):
    # Đọc nội dung của văn bản
    with open(text_path, 'r') as f:
        text_data = f.read()

    # Mã hóa mật khẩu sử dụng SHA-256
    hashed_password = hashlib.sha256(password.encode()).digest()

    # Kết hợp mật khẩu với dữ liệu văn bản
    text_data_with_password = hashed_password + text_data.encode()

    # Chuyển đổi dữ liệu văn bản kết hợp mật khẩu thành chuỗi hex
    encoded_data = text_data_with_password.hex()

    return encoded_data

def main():
    # Đường dẫn đến file văn bản
    text_path = "1.txt"

    # Mật khẩu để mã hóa văn bản
    password = "12345"

    # Mã hóa văn bản thành chuỗi hex với mật khẩu
    encoded_text_data = encode_text_to_hex(text_path, password)

    # Ghi chuỗi hex vào file mới
    with open("encoded_text.txt", 'w') as encoded_file:
        encoded_file.write(encoded_text_data)

    print("Văn bản đã được mã hóa và ghi vào file encoded_text.txt")

if __name__ == "__main__":
    main()
