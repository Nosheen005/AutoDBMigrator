# Dummy data for testing TableEditor layout

tables = {
    "Customers": ["CustomerID", "Name", "Email", "Phone", "Address"],
    "Orders": ["OrderID", "CustomerID", "OrderDate", "TotalAmount"],
    "Products": ["ProductID", "ProductName", "Category", "Price", "Stock", "Supplier"],
    "Employees": ["EmployeeID", "FirstName", "LastName", "Title", "Email", "Phone"],
    "Shippers": ["ShipperID", "CompanyName", "Phone"]
}

CustomerID = {typ: "TEXT", length: 55, key: "pk", null: False}

CustomerID2 = {typ = "TEXT", key = "fk", ref = "Customers"[CustomerID]}

"Customers": [CustomerID, "Name", "Email", "Phone", "Address"],
    "Orders": ["OrderID", CustomerID2, "OrderDate", "TotalAmount"],
    "Products": ["ProductID", "ProductName", "Category", "Price", "Stock", "Supplier"],
    "Employees": ["EmployeeID", "FirstName", "LastName", "Title", "Email", "Phone"],
    "Shippers": ["ShipperID", "CompanyName", "Phone"]
}

workingdata[table][column][columndetail] = value


workingdata = {
    tables1 = {
    "Customers": {"CustomerID": "Value",
                  "Name": "Value",
                  "Email": "Value",
                  "Phone": "Value",
                  "Address": "Value"},
    "Orders": ["OrderID", "CustomerID", "OrderDate", "TotalAmount"],
    "Products": ["ProductID", "ProductName", "Category", "Price", "Stock", "Supplier"],
    "Employees": ["EmployeeID", "FirstName", "LastName", "Title", "Email", "Phone"],
    "Shippers": ["ShipperID", "CompanyName", "Phone"]
},
    tables2 = {
    "Customers": ["CustomerID", "Name", "Email", "Phone", "Address"],
    "Orders": ["OrderID", "CustomerID", "OrderDate", "TotalAmount"],
    "Products": ["ProductID", "ProductName", "Category", "Price", "Stock", "Supplier"],
    "Employees": ["EmployeeID", "FirstName", "LastName", "Title", "Email", "Phone"],
    "Shippers": ["ShipperID", "CompanyName", "Phone"]
}
}