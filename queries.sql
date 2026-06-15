/* 
Query 1: Xu hướng số đơn hàng theo tháng
Mục đích: Xem tháng nào có nhiều đơn nhất
Bảng: orders
*/

SELECT 
    TO_CHAR(DATE_TRUNC('month', order_purchase_timestamp), 'YYYY-MM') AS month,
    COUNT(*) AS total_orders
FROM orders
GROUP BY DATE_TRUNC('month', order_purchase_timestamp)
ORDER BY month

/*
Query 2: Top thành phố có nhiều khách hàng nhất
Mục đích: Xem khách hàng tập trung ở đâu
Bảng: customers
*/

SELECT 
    customer_city,
    COUNT(*) AS total_customers
FROM customers
GROUP BY customer_city
ORDER BY total_customers DESC

/*
Query 3: Trung bình điểm đánh giá theo tháng
Mục đích: Xem chất lượng dịch vụ thay đổi theo thời gian
Bảng: order_reviews
*/

SELECT 
    TO_CHAR(DATE_TRUNC('month', review_creation_date), 'YYYY-MM') AS month,
    ROUND(AVG(review_score), 3) AS avg_score
FROM order_reviews
GROUP BY DATE_TRUNC('month', review_creation_date)
ORDER BY month

/*
Query 4: Top 10 category sản phẩm bán chạy nhất
Mục đích: Xem category nào được mua nhiều nhất
Bảng: order_items, products, category_translation
*/

SELECT 
    ct.product_category_name_english,
    COUNT(*) AS total_sold
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN category_translation ct ON p.product_category_name = ct.product_category_name
GROUP BY ct.product_category_name_english
ORDER BY total_sold DESC
LIMIT 10

/*
Query 5: Top 10 seller có doanh thu cao nhất
Mục đích: Xem seller nào bán được nhiều tiền nhất
Bảng: order_items, sellers
*/

SELECT 
    s.seller_id,
    s.seller_city,
    ROUND(SUM(oi.price)::numeric, 3) AS total_revenue
FROM order_items oi
JOIN sellers s ON oi.seller_id = s.seller_id
GROUP BY s.seller_id, s.seller_city
ORDER BY total_revenue DESC
LIMIT 10