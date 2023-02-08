USE stock_data;
SELECT * FROM stock ORDER BY ticker_date;

DELETE FROM stock WHERE ticker_date='2023-02-07' and symbol="META";


