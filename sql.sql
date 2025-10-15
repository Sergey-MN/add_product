2.1.
SELECT name, SUM(op.quantity * p.price) as total_sum
FROM orders_products op
JOIN orders o ON o.id = op.order_id
JOIN customers c ON c.id = o.customer_id
JOIN products p ON op.product_id = p.id
GROUP BY c.id, c.name

2.2.
SELECT COUNT(sub.title)
FROM category_tree super
JOIN category_tree sub
	ON super.id = sub.supercategory_id
WHERE super.supercategory_id IS NULL

2.3.1.
SELECT p.title, SUM(op.quantity) as total_sold
FROM orders_products op
JOIN orders o ON o.id = op.order_id
JOIN products p ON op.product_id = p.id
WHERE o.created_at >= NOW() - INTERVAL '1 month'
GROUP BY p.title

2.3.2.
1) Частичный индекс на поле created_at для последнего месяца
2) Сначала выбрать все заказы за последний месяц, после джоинить с остальными таблицами
3) Создать отдельную таблицу с количеством проданных товаров и обновлять ее каждый день(нужной переодичностью)
4) Разбить на партиции по дате

