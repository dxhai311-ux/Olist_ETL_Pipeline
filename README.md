# Olist ETL Pipeline

End-to-end ETL pipeline xử lý dữ liệu thương mại điện tử Brazil từ CSV sang PostgreSQL.

---

## Tech Stack

- **Python** — Pandas, SQLAlchemy, python-dotenv
- **PostgreSQL** — data warehouse
- **Dataset** — [Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (~1.5 triệu records, 9 bảng)

---

## Cấu trúc project

```
Olist_ETL_Pipeline/
├── data/           # Raw CSV files (9 files)
├── db.py           # Database connection
├── etl.py          # Extract, Transform, Load logic
├── main.py         # Pipeline orchestration
└── queries.sql     # SQL analysis queries
```

---

## Pipeline

```
CSV Files → Extract → Transform → Load → PostgreSQL
```

### Transform logic

| Bảng | Xử lý |
|---|---|
| `orders` | Lọc delivered, drop NULL, convert datetime, tính delivery_delay |
| `customers`, `sellers`, `category_translation` | Drop duplicate theo primary key |
| `products` | Drop duplicate, drop NULL ở category |
| `order_items`, `order_reviews` | Drop duplicate theo composite key, convert datetime |
| `order_payments` | Drop duplicate theo composite key |
| `geolocation` | Aggregate theo zip code — mean lat/lng, mode city/state |

---

## SQL Analysis

10 queries phân tích trong `queries.sql`:

| Query | Mô tả | Kỹ thuật |
|---|---|---|
| 1 | Xu hướng đơn hàng theo tháng | `DATE_TRUNC`, `TO_CHAR` |
| 2 | Top thành phố có nhiều khách nhất | `GROUP BY`, `COUNT` |
| 3 | Trung bình điểm đánh giá theo tháng | `AVG`, `ROUND` |
| 4 | Top 10 category bán chạy nhất | `JOIN` 3 bảng |
| 5 | Top 10 seller doanh thu cao nhất | `SUM`, `JOIN` |
| 6 | Tổng giao hàng sớm/đúng/trễ hạn | `CASE WHEN` |
| 7 | Tỉ lệ % giao hàng sớm/đúng/trễ hạn | `Window Function` |
| 8 | Doanh thu trung bình theo tháng | `AVG`, `JOIN` |
| 9 | Top 10 seller tỉ lệ 5 sao cao nhất | `HAVING`, `COUNT(DISTINCT)` |
| 10 | Top 5 category doanh thu theo tháng | `CTE`, `RANK() OVER(PARTITION BY)` |

---

## Key Learnings

- ETL pipeline design và implementation
- Data cleaning với Pandas — null handling, deduplication, type conversion
- PostgreSQL connection với SQLAlchemy
- SQL từ cơ bản đến nâng cao — Window Functions, CTE, multi-table JOIN
