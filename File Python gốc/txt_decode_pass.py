import hashlib

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
        print("Mật khẩu không đúng.")
        return

    # Giải mã dữ liệu văn bản
    return encrypted_data.decode()

def main():
    # Đọc chuỗi hex từ file đã mã hóa
    with open("encoded_text.txt", 'r') as encoded_file:
        encoded_text_data = encoded_file.read().strip()

    # Nhập mật khẩu từ người dùng
    password_input = input("Nhập mật khẩu để giải mã: ")

    # Giải mã dữ liệu văn bản
    decoded_text_data = decode_hex_to_text(encoded_text_data, password_input)

    if decoded_text_data:
        # Ghi dữ liệu văn bản đã giải mã vào file mới
        with open("decoded_text.txt", 'w') as decoded_file:
            decoded_file.write(decoded_text_data)
        print("Dữ liệu văn bản đã được giải mã và ghi vào file decoded_text.txt.")

if __name__ == "__main__":
    main()
