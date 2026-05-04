# Demo 2026 Sales & Marketing Dashboard

Dashboard Streamlit public-ready cho dữ liệu kinh doanh và marketing năm 2026 của công ty Demo.

## Nội dung repo

- `app.py`: app Streamlit chạy trực tiếp.
- `data/demo_sales_2026.csv`: dữ liệu sales đã làm sạch và ẩn danh.
- `data/demo_kpi_2026.csv`: dữ liệu KPI đã đối soát Actual và ẩn danh.
- `requirements.txt`: dependencies để deploy local hoặc Streamlit Community Cloud.

## Tính năng chính

- Chỉ giữ bộ lọc thời gian để giao diện tập trung, dễ xem.
- Dashboard doanh số:
  - Tổng doanh số, % đạt KPI, tổng deal, giá trị deal trung bình.
  - Doanh số theo tháng, phòng ban, vùng miền, nhu cầu, loại hình căn hộ.
  - Top nhân sự theo doanh số và theo % KPI.
  - KPI vs Actual theo phòng ban.
- Dashboard marketing:
  - Doanh thu theo nguồn lead.
  - Số lead/cơ hội theo nguồn.
  - Proxy conversion rate.
  - Doanh thu trung bình trên mỗi lead.
  - Bubble chart so sánh hiệu suất kênh.
- Insight tự động:
  - Xu hướng kinh doanh.
  - Top performer và mức độ tập trung doanh số.
  - Kênh marketing hiệu quả nhất.
  - Cảnh báo KPI dưới 80%.
  - Khuyến nghị vận hành.

## Chạy local

```powershell
pip install -r requirements.txt
streamlit run app.py
```

## Deploy lên Streamlit Community Cloud

1. Push repo này lên GitHub public.
2. Vào [Streamlit Community Cloud](https://share.streamlit.io/).
3. Chọn repo `lieuaof0412/demo-dashboard-2026`.
4. Main file path: `app.py`.
5. Deploy.

## Ghi chú dữ liệu

- Bản public này dùng dữ liệu đã được chuẩn hóa và ẩn danh.
- KPI `Actual` được tính lại từ dữ liệu sales để đảm bảo dashboard nhất quán.
- Chỉ số conversion marketing là proxy từ `opportunity_id` trong dữ liệu hợp đồng, không phải funnel lead thô.
