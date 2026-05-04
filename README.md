# Demo 2026 Sales & Marketing Dashboard

Dashboard Streamlit để làm sạch dữ liệu doanh số/KPI và phân tích hiệu quả kinh doanh, marketing cho công ty Demo năm 2026.

## Thành phần chính

- ETL cho 2 file đầu vào Excel/CSV: tự phát hiện file sales và file KPI trong project hoặc thư mục con.
- Chuẩn hóa ngày, số, text, phòng ban, nguồn lead, loại hình căn hộ, vùng miền.
- Dashboard doanh số:
  - Tổng doanh số
  - % đạt KPI toàn công ty
  - Tổng deal / khách hàng
  - Doanh số theo tháng, BU, vùng miền, nhu cầu, loại hình căn hộ
  - KPI vs Actual theo BU
  - Top nhân sự theo doanh số và theo % KPI
- Dashboard marketing:
  - Doanh thu theo nguồn lead
  - Số lead / cơ hội theo nguồn
  - Proxy conversion rate
  - Doanh thu trung bình / lead
  - Bảng so sánh hiệu quả nhóm kênh
- Insight tự động, forecast ngắn hạn và alert KPI.

## Cấu trúc project

- `app.py`
- `ff_dashboard/data.py`
- `ff_dashboard/analytics.py`
- `requirements.txt`

## Cách chạy

1. Cài Python 3.11+ nếu máy chưa có.
2. Cài dependencies:

```powershell
pip install -r requirements.txt
```

3. Chạy app:

```powershell
streamlit run app.py
```

4. Mở URL Streamlit được in ra terminal.

## Ghi chú dữ liệu

- App đang ưu tiên `Doanh số trước VAT` làm Actual để đồng bộ KPI.
- App hỗ trợ cả tên file tiếng Việt hiện tại và tên file ASCII kiểu `sales_2026_data.csv`, `sales_2026_kpi.csv`.
- File KPI có một số dòng `Doanh số` lệch so với file giao dịch chi tiết; app tự tái tính Actual từ dữ liệu sales và giữ lại cột chênh lệch để audit.
- Dashboard marketing hiện dùng `opportunity_id` suy ra từ dữ liệu hợp đồng như một proxy cho lead/cơ hội, vì input hiện tại chưa có file lead funnel thô.

## Mở rộng tiếp

- Bổ sung page forecast sâu hơn theo BU.
- Thêm phân tầng KPI theo tuần nếu có dữ liệu mục tiêu tuần.
- Kết nối upload file trực tiếp qua Streamlit thay vì auto-discovery trong thư mục.
