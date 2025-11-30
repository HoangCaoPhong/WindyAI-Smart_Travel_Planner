# TEST CASES THỦ CÔNG - HỆ THỐNG NHẬN DIỆN ĐỊA ĐIỂM DU LỊCH VIỆT NAM

## Thông tin chung
- **Dự án**: Smart Travel Project - Nhận diện địa điểm du lịch TP.HCM
- **Model**: ResNet18 với 21 lớp địa điểm
- **Ngày test**: 30/11/2025

---

## TEST CASE 1: Kiểm tra Model Load thành công
**Mục đích**: Xác nhận model được load và sẵn sàng sử dụng

### Input:
```python
python predict_vn.py
```

### Expected Output:
```
Using device: cpu (hoặc cuda)
Số lớp: 21
Classes: ['Bitexco', 'Bưu điện thành phố', ...]
```

### Kết quả: ☐ Pass ☐ Fail

---

## TEST CASE 2: Dự đoán ảnh Bitexco
**Mục đích**: Nhận diện đúng tòa nhà Bitexco Financial Tower

### Input:
```python
python predict_vn.py data/val/Bitexco/bitexco_001.jpg
```

### Expected Output:
```
Kết quả: Bitexco (độ tin cậy = >70.00%)
```

### Kết quả: ☐ Pass ☐ Fail
**Ghi chú**: _______________________________

---

## TEST CASE 3: Dự đoán ảnh Chợ Bến Thành
**Mục đích**: Nhận diện đúng Chợ Bến Thành

### Input:
```python
python predict_vn.py data/val/Chợ Bến Thành/benthanhmarket_001.jpg
```

### Expected Output:
```
Kết quả: Chợ Bến Thành (độ tin cậy = >70.00%)
```

### Kết quả: ☐ Pass ☐ Fail
**Ghi chú**: _______________________________

---

## TEST CASE 4: Dự đoán ảnh Nhà thờ Đức Bà
**Mục đích**: Nhận diện đúng Nhà thờ Đức Bà

### Input:
```python
python predict_vn.py data/val/Nhà thờ Đức Bà/cathedral_001.jpg
```

### Expected Output:
```
Kết quả: Nhà thờ Đức Bà (độ tin cậy = >70.00%)
```

### Kết quả: ☐ Pass ☐ Fail
**Ghi chú**: _______________________________

---

## TEST CASE 5: Dự đoán ảnh Dinh Độc Lập
**Mục đích**: Nhận diện đúng Dinh Độc Lập

### Input:
```python
python predict_vn.py data/val/Dinh Độc Lập/independence_palace_001.jpg
```

### Expected Output:
```
Kết quả: Dinh Độc Lập (độ tin cậy = >70.00%)
```

### Kết quả: ☐ Pass ☐ Fail
**Ghi chú**: _______________________________

---

## TEST CASE 6: Dự đoán ảnh Landmark 81
**Mục đích**: Nhận diện đúng Landmark 81

### Input:
```python
python predict_vn.py data/val/Landmark 81/landmark81_001.jpg
```

### Expected Output:
```
Kết quả: Landmark 81 (độ tin cậy = >70.00%)
```

### Kết quả: ☐ Pass ☐ Fail
**Ghi chú**: _______________________________

---

## TEST CASE 7: Dự đoán ảnh Bưu điện Thành phố
**Mục đích**: Nhận diện đúng Bưu điện TP.HCM

### Input:
```python
python predict_vn.py data/val/Bưu điện thành phố/postoffice_001.jpg
```

### Expected Output:
```
Kết quả: Bưu điện thành phố (độ tin cậy = >70.00%)
```

### Kết quả: ☐ Pass ☐ Fail
**Ghi chú**: _______________________________

---

## TEST CASE 8: Dự đoán ảnh Bảo tàng Chứng tích Chiến tranh
**Mục đích**: Nhận diện đúng Bảo tàng Chứng tích Chiến tranh

### Input:
```python
python predict_vn.py data/val/Bảo tàng Chứng tích Chiến tranh/warmuseum_001.jpg
```

### Expected Output:
```
Kết quả: Bảo tàng Chứng tích Chiến tranh (độ tin cậy = >70.00%)
```

### Kết quả: ☐ Pass ☐ Fail
**Ghi chú**: _______________________________

---

## TEST CASE 9: Dự đoán ảnh Nhà hát Thành phố
**Mục đích**: Nhận diện đúng Nhà hát TP.HCM (Opera House)

### Input:
```python
python predict_vn.py data/val/Nhà hát Thành phố/operahouse_001.jpg
```

### Expected Output:
```
Kết quả: Nhà hát Thành phố (độ tin cậy = >70.00%)
```

### Kết quả: ☐ Pass ☐ Fail
**Ghi chú**: _______________________________

---

## TEST CASE 10: Dự đoán ảnh Phố đi bộ Nguyễn Huệ
**Mục đích**: Nhận diện đúng Phố đi bộ Nguyễn Huệ

### Input:
```python
python predict_vn.py data/val/Phố đi bộ Nguyễn Huệ/nguyenhue_001.jpg
```

### Expected Output:
```
Kết quả: Phố đi bộ Nguyễn Huệ (độ tin cậy = >70.00%)
```

### Kết quả: ☐ Pass ☐ Fail
**Ghi chú**: _______________________________

---

## TEST CASE 11: Dự đoán ảnh Bến Nhà Rồng
**Mục đích**: Nhận diện đúng Bến Nhà Rồng (Bảo tàng Hồ Chí Minh)

### Input:
```python
python predict_vn.py data/val/Bến Nhà Rồng/bennharong_001.jpg
```

### Expected Output:
```
Kết quả: Bến Nhà Rồng (độ tin cậy = >70.00%)
```

### Kết quả: ☐ Pass ☐ Fail
**Ghi chú**: _______________________________

---

## TEST CASE 12: Dự đoán ảnh Suối Tiên
**Mục đích**: Nhận diện đúng Công viên Suối Tiên

### Input:
```python
python predict_vn.py data/val/Suối Tiên/suoitien_001.jpg
```

### Expected Output:
```
Kết quả: Suối Tiên (độ tin cậy = >70.00%)
```

### Kết quả: ☐ Pass ☐ Fail
**Ghi chú**: _______________________________

---

## TEST CASE 13: Dự đoán ảnh Thảo cầm viên
**Mục đích**: Nhận diện đúng Thảo cầm viên Sài Gòn (Zoo)

### Input:
```python
python predict_vn.py data/val/Thảo cầm viên/zoo_001.jpg
```

### Expected Output:
```
Kết quả: Thảo cầm viên (độ tin cậy = >70.00%)
```

### Kết quả: ☐ Pass ☐ Fail
**Ghi chú**: _______________________________

---

## TEST CASE 14: Dự đoán ảnh UBND TP.HCM
**Mục đích**: Nhận diện đúng Tòa nhà UBND TP.HCM

### Input:
```python
python predict_vn.py data/val/UBND _tp Hồ Chí Minh/ubnd_001.jpg
```

### Expected Output:
```
Kết quả: UBND _tp Hồ Chí Minh (độ tin cậy = >70.00%)
```

### Kết quả: ☐ Pass ☐ Fail
**Ghi chú**: _______________________________

---

## TEST CASE 15: Dự đoán ảnh Đường sách Nguyễn Văn Bình
**Mục đích**: Nhận diện đúng Đường sách Nguyễn Văn Bình

### Input:
```python
python predict_vn.py data/val/Đường sách Nguyễn Văn Bình/booksstreet_001.jpg
```

### Expected Output:
```
Kết quả: Đường sách Nguyễn Văn Bình (độ tin cậy = >70.00%)
```

### Kết quả: ☐ Pass ☐ Fail
**Ghi chú**: _______________________________

---

## TEST CASE 16: Dự đoán ảnh không tồn tại (Error Case)
**Mục đích**: Kiểm tra xử lý lỗi khi file không tồn tại

### Input:
```python
python predict_vn.py nonexistent_image.jpg
```

### Expected Output:
```
FileNotFoundError: [Errno 2] No such file or directory: 'nonexistent_image.jpg'
hoặc
Error: Cannot open image file
```

### Kết quả: ☐ Pass ☐ Fail
**Ghi chú**: _______________________________

---

## TEST CASE 17: Dự đoán ảnh định dạng PNG
**Mục đích**: Kiểm tra hỗ trợ định dạng PNG

### Input:
```python
python predict_vn.py test_image.png
```

### Expected Output:
```
Kết quả: [Tên địa điểm] (độ tin cậy = XX.XX%)
```

### Kết quả: ☐ Pass ☐ Fail
**Ghi chú**: _______________________________

---

## TEST CASE 18: Dự đoán ảnh kích thước lớn (4K)
**Mục đích**: Kiểm tra xử lý ảnh kích thước lớn

### Input:
```python
python predict_vn.py large_image_3840x2160.jpg
```

### Expected Output:
```
Kết quả: [Tên địa điểm] (độ tin cậy = XX.XX%)
```

### Kết quả: ☐ Pass ☐ Fail
**Ghi chú**: Model tự động resize về 224x224

---

## TEST CASE 19: Dự đoán ảnh kích thước nhỏ (100x100)
**Mục đích**: Kiểm tra xử lý ảnh kích thước nhỏ

### Input:
```python
python predict_vn.py small_image_100x100.jpg
```

### Expected Output:
```
Kết quả: [Tên địa điểm] (độ tin cậy = XX.XX%)
```

### Kết quả: ☐ Pass ☐ Fail
**Ghi chú**: Model tự động resize về 224x224

---

## TEST CASE 20: Test tất cả 21 địa điểm
**Mục đích**: Kiểm tra model nhận diện đúng tất cả 21 địa điểm

### Input:
Chạy lần lượt với mỗi địa điểm:
```python
python predict_vn.py data/val/[Tên địa điểm]/image_001.jpg
```

### Danh sách 21 địa điểm cần test:
1. ☐ Bitexco
2. ☐ Bưu điện thành phố
3. ☐ Bảo tàng Chứng tích Chiến tranh
4. ☐ Bảo tàng lịch sử tpHCM
5. ☐ Bảo tàng mỹ thuật tpHCM
6. ☐ Bến Bạch Đằng
7. ☐ Bến Nhà Rồng
8. ☐ Chợ Bến Thành
9. ☐ Công viên 30 tháng 4
10. ☐ Cầu Ánh Sao
11. ☐ Dinh Độc Lập
12. ☐ Ga Sài Gòn
13. ☐ Landmark 81
14. ☐ Nhà hát Thành phố
15. ☐ Nhà thờ Đức Bà
16. ☐ Phố đi bộ Nguyễn Huệ
17. ☐ SaiGon Center
18. ☐ Suối Tiên
19. ☐ Thảo cầm viên
20. ☐ UBND _tp Hồ Chí Minh
21. ☐ Đường sách Nguyễn Văn Bình

### Expected Output:
```
Mỗi địa điểm được nhận diện đúng với độ tin cậy > 70%
```

### Kết quả tổng: ☐ Pass ☐ Fail
**Số địa điểm nhận diện đúng**: ___/21

---

## BÁO CÁO TỔNG KẾT

### Thông tin người test:
- **Họ tên**: _______________________________
- **Ngày test**: _______________________________
- **Thời gian**: _______________________________

### Kết quả:
- **Tổng số test cases**: 20
- **Số test Pass**: ___/20
- **Số test Fail**: ___/20
- **Tỷ lệ thành công**: ___%

### Các lỗi phát hiện:
1. _______________________________
2. _______________________________
3. _______________________________

### Nhận xét chung:
_________________________________________
_________________________________________
_________________________________________

### Đề xuất cải thiện:
_________________________________________
_________________________________________
_________________________________________

---

## HƯỚNG DẪN SỬ DỤNG

### Chuẩn bị:
1. Đảm bảo đã cài đặt Python và các thư viện cần thiết
2. Đảm bảo file `model_vietnam.pth` và `classes.txt` tồn tại
3. Đảm bảo thư mục `data/val/` có đủ ảnh test

### Cách test:
1. Mở Terminal/Command Prompt
2. Di chuyển đến thư mục dự án
3. Chạy lệnh test theo từng test case
4. Ghi nhận kết quả vào ô checkbox
5. Ghi chú nếu có vấn đề

### Tiêu chí đánh giá:
- **Pass**: Kết quả đúng như expected output
- **Fail**: Kết quả khác expected output hoặc có lỗi

### Lưu ý:
- Độ tin cậy có thể dao động, chấp nhận sai số ±5%
- Một số địa điểm tương tự có thể bị nhầm lẫn (vd: bảo tàng)
- Ghi chú chi tiết các trường hợp Fail để cải thiện model
