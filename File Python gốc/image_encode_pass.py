import hashlib

def encode_image_to_hex(image_path, password):
    # Đọc nội dung của hình ảnh dưới dạng byte
    with open(image_path, 'rb') as f:
        image_data = f.read()

    # Mã hóa mật khẩu sử dụng SHA-256
    hashed_password = hashlib.sha256(password.encode()).digest()

    # Kết hợp mật khẩu với dữ liệu hình ảnh
    image_data_with_password = hashed_password + image_data

    # Chuyển đổi dữ liệu hình ảnh kết hợp mật khẩu thành chuỗi hex
    encoded_data = image_data_with_password.hex()

    return encoded_data

def main():
    # Đường dẫn đến hình ảnh
    image_path = "1.png"

    # Mật khẩu để mã hóa hình ảnh
    password = "Datpro2691"

    # Mã hóa hình ảnh thành chuỗi hex với mật khẩu
    encoded_image_data = encode_image_to_hex(image_path, password)

    # Ghi chuỗi hex vào file mới
    with open("encoded_image.txt", 'w') as encoded_file:
        encoded_file.write(encoded_image_data)

    print("Hình ảnh đã được mã hóa và ghi vào file encoded_image.txt")

if __name__ == "__main__":
    main()
