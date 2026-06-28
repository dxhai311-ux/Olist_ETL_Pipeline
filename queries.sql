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

/*
Query 6: Tổng giao hàng sớm, đúng hạn, trễ hạn
Mục đích: Xem chất lượng giao hàng của Olist
Bảng: orders
*/
SELECT
    CASE 
        WHEN delivery_delay < 0
            THEN 'Early term'
        WHEN delivery_delay > 0 
            THEN 'Late deadline'
        ELSE 'On time'
    END AS delivery_status,
    COUNT(*) AS total
FROM orders
GROUP BY 1

/*
Query 7: Tỉ lệ % giao hàng sớm, đúng hạn, trễ hạn
Mục đích: Xem chất lượng giao hàng của Olist
Bảng: orders
*/
SELECT 
    CASE 
        WHEN delivery_delay < 0
            THEN 'Early tern'
        WHEN delivery_delay > 0 
            THEN 'Late deadline'
        ELSE 'On time'
    END AS delivery_status,
    COUNT(*) AS total,
    ROUND((COUNT(*) * 100.0) / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM orders
GROUP BY 1
ORDER BY percentage DESC

/*
Query 8: Top 10 seller có tỷ lệ đánh giá 5 sao cao nhất
Mục đích:
- Đánh giá chất lượng dịch vụ của seller
- Tìm những seller có tỷ lệ hài lòng cao nhất
- Chỉ xét seller có trên 20 review để đảm bảo độ tin cậy
Bảng:sellers, order_items, order_reviews
*/
SELECT 
      s.seller_id,
      COUNT(*) AS total_review,
      COUNT(
        CASE 
            WHEN orr.review_score = 5
            THEN 1
        END
      ) AS five_star_reviews,
      ROUND(
        COUNT(
            CASE
                WHEN orr.review_score = 5
                THEN 1
            END
        ) * 100.0 
        / COUNT(*), 
        2) AS five_star_rate
FROM sellers s 
JOIN order_items oi ON s.seller_id = oi.seller_id 
JOIN order_reviews orr ON oi.order_id = orr.order_id 
GROUP BY s.seller_id 
HAVING COUNT(DISTINCT orr.review_id) > 20
ORDER BY five_star_rate DESC
LIMIT 10;

/*
Query 9: Top 10 seller có doanh thu cao nhất
Mục đích:
- Xác định những seller tạo ra doanh thu cao nhất.
- Thống kê số lượng đơn hàng và tổng doanh thu của từng seller.
- Phục vụ phân tích hiệu quả kinh doanh và xếp hạng seller.
Bảng:
- sellers
- order_items
*/
SELECT 
        s.seller_id,
        COUNT(DISTINCT order_id) AS total_orders,
        ROUND(SUM(price)::numeric, 3) AS total_revenue
FROM sellers s
JOIN order_items oi ON s.seller_id = oi.seller_id 
GROUP BY s.seller_id 
ORDER BY total_revenue DESC 
LIMIT 10;

/*
Query 10: Top 5 category doanh thu cao nhất theo từng tháng
Mục đích: Xem category nào dẫn đầu doanh thu mỗi tháng
Bảng: order_items, orders, products, category_translation
Kỹ thuật: CTE 2 tầng + RANK() OVER(PARTITION BY)
*/
WITH monthly_revenue AS(
    SELECT  
            TO_CHAR(DATE_TRUNC('month', order_purchase_timestamp), 'YYYY-MM') AS month,
            ct.product_category_name_english AS category,
            ROUND(SUM(price)::numeric, 3) AS revenue
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id 
    JOIN products p  ON p.product_id = oi.product_id 
    JOIN category_translation ct ON ct.product_category_name = p.product_category_name 
    GROUP BY 1, 2
),
ranked AS(
    SELECT  *,
            RANK() OVER(PARTITION BY month ORDER BY revenue DESC) AS rank
    FROM monthly_revenue 
)
SELECT *
FROM ranked
WHERE rank <= 5
ORDER BY month, rank