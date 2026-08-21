# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

| | |
|---|---|
| Họ và tên | Nguyễn Văn Dương |
| MSSV | 2A202601400 |
| Lớp / Khóa | K4 |
| Repo GitHub | https://github.com/Duongw171/K4-Track2-Day21-2A202601400-NguyenVanDuong |
| Ngày nộp | 21/08/2026 |

---

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do

| Lần chạy | n_estimators | learning_rate | max_depth | f1_score | accuracy |
|---|---|---|---|---|---|
| 1 | 100 | 0.1 | 3 | 0.7109 | 0.8780 |
| 2 | 50 | 0.05 | 2 | 0.6051 | 0.8460 |
| 3 | 200 | 0.1 | 5 | 0.7149 | 0.8740 |

**Bộ siêu tham số đã chọn:** `n_estimators=200`, `learning_rate=0.1`, `max_depth=5`.

**Lý do:** Bộ tham số ở lần 3 đạt điểm `f1_score` cao nhất (0.7149), vượt qua ngưỡng chất lượng (0.65). Mặc dù lần 1 có accuracy nhỉnh hơn một chút (0.8780 so với 0.8740), nhưng lần 3 có F1 vượt trội hơn, chứng tỏ mô hình nhận diện lớp thiểu số (thu nhập cao) tốt hơn. Trong thực nghiệm, `n_estimators` và `learning_rate` có sự đánh đổi rõ rệt: giảm số cây xuống 50 kết hợp learning rate thấp 0.05 ở lần 2 khiến mô hình underfitting, F1 tụt xuống chỉ còn 0.6051 và không vượt qua được quality gate.

---

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Tập dữ liệu Adult có sự mất cân bằng lớp nghiêm trọng khi chỉ có khoảng 24.8% số mẫu thuộc lớp thu nhập cao (>50K). Một mô hình vô dụng luôn dự đoán "thu nhập thấp" cho mọi trường hợp vẫn dễ dàng đạt độ chính xác (accuracy) lên tới 75.2%, nhưng F1-score của lớp dương khi đó sẽ bằng 0.000 vì hoàn toàn không phát hiện được trường hợp thu nhập cao nào. Do đó, accuracy là chỉ số gây hiểu nhầm trong các bài toán mất cân bằng.

F1-score là trung bình điều hòa giữa Precision và Recall, đo lường chính xác khả năng bắt trúng và đúng của mô hình trên lớp thiểu số quan trọng. Khi tính toán, ta bắt buộc phải đánh giá F1 trực tiếp trên lớp dương (không dùng `average="weighted"` hay `average="macro"`), bởi vì trung bình có trọng số sẽ bị lớp đa số (75.2%) kéo điểm lên cao giả tạo và làm mất ý nghĩa kiểm soát chất lượng của pipeline CI/CD.

---

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| Lỗi phân quyền khi DVC push lên AWS S3 (`AccessDenied`). | IAM User ban đầu chưa được gán chính sách quyền đọc/ghi trên S3 Bucket. | Sử dụng IAM Role gán trực tiếp cho máy ảo EC2 để đồng bộ dữ liệu và cấu hình lại bucket policy. |
| Không tương thích phiên bản scikit-learn khi load model trên máy ảo. | Môi trường Python trên local (3.13) khác với Ubuntu trên VM dẫn đến lệch cấu trúc pickle. | Huấn luyện mô hình trực tiếp trong môi trường VM/CI Runner để đảm bảo tính tương thích tuyệt đối. |
| Quá trình cài đặt gói phụ thuộc trên CI/CD bị kéo dài. | Trình quản lý gói pip gặp xung đột phiên bản phụ thuộc giữa dvc-s3 và boto3. | Chỉ định region chuẩn `ap-southeast-2` và tối ưu các câu lệnh cài đặt package trong file workflow cicd.yml. |

---

## 4. So Sánh Bước 2 và Bước 3

| | f1_score | accuracy |
|---|---|---|
| Bước 2 (chỉ `train_batch1`) | 0.7149 | 0.8740 |
| Bước 3 (thêm `train_batch2`) | 0.7128 | 0.8760 |

**Nhận xét:** Khi bổ sung thêm 22.361 mẫu từ `train_batch2`, điểm F1 có sự dao động nhẹ (0.7149 sang 0.7128) do cả hai tập dữ liệu được chia ngẫu nhiên từ cùng một phân phối điều tra dân số, nên dữ liệu mới không bổ sung thêm nhiều biến thiên đặc trưng mới. Tuy nhiên, giá trị cốt lõi là toàn bộ vòng lặp CI/CD đã tự động kích hoạt, huấn luyện và tái triển khai thành công mô hình mà không cần bất kỳ can thiệp thủ công nào.
