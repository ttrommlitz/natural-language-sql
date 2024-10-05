## Database Description and Purpose

Our database is meant to model a store. The database has 4 tables: Users, Products, Orders, and OrderDetails.

## Schema Picture
![Alt text](EF750121-CBE0-4872-BBC8-2FDDE3B5B431_1_201_a.jpeg)

## Sample Question that worked well:

- Question: How much has each user spent all time? I would like to know the user's first name, last name, and total spent
- Model SQL Query: 
```
SELECT Users.FirstName, Users.LastName, SUM(Products.Price * OrderDetails.Quantity) AS TotalSpent
FROM Users
JOIN Orders ON Users.UserID = Orders.UserID
JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
JOIN Products ON OrderDetails.ProductID = Products.ProductID
GROUP BY Users.UserID, Users.FirstName, Users.LastName;
```
- Output:
```
[
  ('Carol', 'Williams', Decimal('150.00')),
  ('Eve', 'Davis', Decimal('3200.00')),
  ('David', 'Brown', Decimal('25.00')),
  ('Bob', 'Johnson', Decimal('900.00')),
  ('Alice', 'Smith', Decimal('1200.00'))
]
```

## Sample Question that did not work well:

- Question: How much total has Alice spent all time?
- Model SQL Query: 
```
SELECT SUM(Product.Price * OrderDetails.Quantity) AS TotalSpent
FROM Users
JOIN Orders ON Users.UserID = Orders.UserID
JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
JOIN Products ON OrderDetails.ProductID = Products.ProductID
WHERE Users.FirstName = 'Alice';
```
- Output: 
```
Traceback (most recent call last):
  File "/Users/tylertrommlitz/Documents/Projects/natural-language-sql-project/main.py", line 54, in execute_query
    cursor.execute(query)
psycopg2.errors.UndefinedTable: missing FROM-clause entry for table "product"
LINE 1: SELECT SUM(Product.Price * OrderDetails.Quantity) AS TotalSp...
```

## Prompting strategies

We tried both zero-shot and few-shot prompting. The few-shot prompting performed vastly better than zero-shot prompting.
Only extremely simple prompts such as "How many orders are there?" worked with zero-shot prompting.
In order to get more complicated prompts such as "What is the total revenue generated from each product category?" an example query and response was needed.

## More Query Examples

All questions use few-shot prompting with one example input and output.
The example question used is
"How much total has Alice spent all time?"

The example query used is
```
SELECT SUM(Price * Quantity) AS TotalSpent
FROM Users JOIN Orders ON Users.UserID = Orders.UserID
JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
JOIN Products ON OrderDetails.ProductID = Products.ProductID
WHERE Users.FirstName = 'Alice';
```

- Question 1: What are the top 3 best-selling products?
- Model SQL Query: 
```
SELECT Products.ProductName, SUM(OrderDetails.Quantity) AS TotalSold
FROM Products
JOIN OrderDetails ON Products.ProductID = OrderDetails.ProductID
GROUP BY Products.ProductName
ORDER BY TotalSold DESC
LIMIT 3;
```

- Output:
```
[
    ('Laptop', 3),
    ('Smartphone', 2),
    ('Wireless Mouse', 1)
]
```

- Question 2: Which users have placed the most orders?
- Model SQL Query: 
```
SELECT FirstName, LastName, COUNT(OrderID) AS TotalOrders FROM Users JOIN Orders ON Users.UserID = Orders.UserID GROUP BY Users.UserID ORDER BY TotalOrders DESC;
```

- Output:
```
[
    ('Carol', 'Williams', 1),
    ('Eve', 'Davis', 1),
    ('David', 'Brown', 1),
    ('Bob', 'Johnson', 1),
    ('Alice', 'Smith', 1)
]
```

- Question 3: What is the total revenue generated from each product category?
Count any order status, whether it is completed or not.
- Model SQL Query: 
```
SELECT Products.Category, SUM(Products.Price * OrderDetails.Quantity) AS TotalRevenue
FROM Products
JOIN OrderDetails ON Products.ProductID = OrderDetails.ProductID
JOIN Orders ON OrderDetails.OrderID = Orders.OrderID
GROUP BY Products.Category;
```

- Output:
```
[
    ('Furniture', Decimal('150.00')),
    ('Home Appliances', Decimal('100.00')),
    ('Electronics', Decimal('5225.00'))
]
```

- Question 4: What are the details of all orders placed by Bob Johnson?
- Model SQL Query: 
```
SELECT Orders.OrderID, Orders.OrderDate, Orders.Status, Products.ProductName, Products.Price, OrderDetails.Quantity
FROM Users
JOIN Orders ON Users.UserID = Orders.UserID
JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
JOIN Products ON OrderDetails.ProductID = Products.ProductID
WHERE Users.FirstName = 'Bob' AND Users.LastName = 'Johnson';
```

- Output:
```
[
    (2, datetime.datetime(2023, 7, 20, 15, 30), 'Shipped', 'Smartphone', Decimal('800.00'), 1),
    (2, datetime.datetime(2023, 7, 20, 15, 30), 'Shipped', 'Coffee Maker', Decimal('100.00'), 1)
]
```

- Question 5: What is the average order value?
- Model SQL Query: 
```
SELECT AVG(Price * Quantity) AS AverageOrderValue FROM Orders
JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
JOIN Products ON OrderDetails.ProductID = Products.ProductID;
```

- Output:
```
[
    (Decimal('782.1428571428571429'),)
]
```

- Question 6: Which person spent the most amount of money?
- Model SQL Query: 
```
SELECT CONCAT(Users.FirstName, ' ', Users.LastName) AS Person, SUM(Price * Quantity) AS TotalSpent
FROM Users
JOIN Orders ON Users.UserID = Orders.UserID
JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
JOIN Products ON OrderDetails.ProductID = Products.ProductID
GROUP BY Users.UserID
ORDER BY TotalSpent DESC
LIMIT 1;
```

- Output:
```
[
    ('Eve Davis', Decimal('3200.00'))
]
```

- Question 7: Who placed the most recent order?
- Model SQL Query: 
```
SELECT FirstName, LastName
FROM Users
JOIN Orders ON Users.UserID = Orders.UserID
ORDER BY OrderDate DESC
LIMIT 1;
```

- Output:
```
[
    ('Eve', 'Davis')
]
```
