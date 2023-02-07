CREATE DATABASE stock_data;
USE stock_data;


CREATE TABLE stock(
	symbol varchar(10),
    ticker_date DATE,
    open_price DECIMAL(8,2),
    high_price DECIMAL(8,2),
    low_price DECIMAL(8,2),
    close_price DECIMAL(8,2),
    volume int,
    PRIMARY KEY(symbol, ticker_date)
);
USE stock_data;

CREATE USER 'stock_user'@'localhost' IDENTIFIED by 'letmein';
GRANT ALL ON stock_data.* to 'stock_user'@'localhost' WITH GRANT OPTION;