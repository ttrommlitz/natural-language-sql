-- Insert Users
INSERT INTO Users (FirstName, LastName, Email)
VALUES ('Alice', 'Smith', 'alice@example.com'),
('Bob', 'Johnson', 'bob@example.com'),
('Carol', 'Williams', 'carol@example.com'),
('David', 'Brown', 'david@example.com'),
('Eve', 'Davis', 'eve@example.com'); 

-- Insert Products 

INSERT INTO Products (ProductName, Price, StockQuantity, Category) 
VALUES ('Laptop', 1200.00, 50, 'Electronics'),
('Smartphone', 800.00, 100, 'Electronics'),
('Coffee Maker', 100.00, 200, 'Home Appliances'),
('Desk Chair', 150.00, 75, 'Furniture'),
('Wireless Mouse', 25.00, 150, 'Electronics'); 

-- Insert Orders

INSERT INTO Orders (UserID, OrderDate, Status) 
VALUES (1, '2023-06-15 12:00:00', 'Completed'),
(2, '2023-07-20 15:30:00', 'Shipped'),
(3, '2023-08-10 11:00:00', 'Processing'),
(4, '2023-09-05 09:15:00', 'Completed'),
(5, '2023-09-20 13:45:00', 'Canceled'); 

-- Insert OrderDetails

INSERT INTO OrderDetails (OrderID, ProductID, Quantity)
VALUES (1, 1, 1),
(2, 2, 1),
(2, 3, 1),
(3, 4, 1),
(4, 5, 1),
(5, 1, 2),
(5, 2, 1);