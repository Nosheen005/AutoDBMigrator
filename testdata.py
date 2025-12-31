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

{'TestTable1': {
    'Flera kommuner': {
        'type': 'INTEGER', 
        'length': '255', 
        'nullable': 'False', 
        'key': 'Foreign Key', 
        'auto_increment': 'False', 
        'references_table': 'TestTable2', 
        'references_column': 'Flera kommuner', 
        'unique': 'False'
        }, 
    'Antal kommuner': {
        'type': 'VARCHAR', 
        'length': '255', 
        'nullable': 'False', 
        'key': 'None', 
        'auto_increment': 'False', 
        'references_table': '', 
        'references_column': '', 
        'unique': 'False'
        }, 
    'Län': {
        'type': 'VARCHAR', 
        'length': '255', 
        'nullable': 'False', 
        'key': 'None', 
        'auto_increment': 'False', 
        'references_table': '', 
        'references_column': '', 
        'unique': 'False'
        }, 
    'Kommun': {
        'type': 'VARCHAR', 
        'length': '255', 
        'nullable': 'False', 
        'key': 'None', 
        'auto_increment': 'False', 
        'references_table': '', 
        'references_column': '', 
        'unique': 'False'
        }, 
    'Utbildningsområde': {
        'type': 'VARCHAR', 
        'length': '255', 
        'nullable': 'False', 
        'key': 'None', 
        'auto_increment': 'False', 
        'references_table': '', 
        'references_column': '', 
        'unique': 'False'
        }, 
    'Utbildningsnamn': {
        'type': 'VARCHAR', 
        'length': '255', 
        'nullable': 'False', 
        'key': 'None', 
        'auto_increment': 'False', 
        'references_table': '', 
        'references_column': '', 
        'unique': 'False'
        }, 
    'Typ av examen': {
        'type': 'VARCHAR', 
        'length': '255', 
        'nullable': 'False', 
        'key': 'None', 
        'auto_increment': 'False', 
        'references_table': '', 
        'references_column': '', 
        'unique': 'False'
        }, 
    'YH-poäng': {
        'type': 'VARCHAR', 
        'length': '255', 
        'nullable': 'False', 
        'key': 'None', 
        'auto_increment': 'False', 
        'references_table': '', 
        'references_column': '', 
        'unique': 'False'
        }, 
    'Studieform': {
        'type': 'VARCHAR', 
        'length': '255', 
        'nullable': 'False', 
        'key': 'None', 
        'auto_increment': 'False', 
        'references_table': '', 
        'references_column': '', 
        'unique': 'False'
        }, 
    'Studietakt %': {
        'type': 'VARCHAR', 
        'length': '255', 
        'nullable': 'False', 
        'key': 'None', 
        'auto_increment': 'False', 
        'references_table': '', 
        'references_column': '', 
        'unique': 'False'
        }, 
    'Utbildningsanordnare administrativ enhet': {
        'type': 'VARCHAR', 
        'length': '255', 
        'nullable': 'False', 
        'key': 'None', 
        'auto_increment': 'False', 
        'references_table': '', 
        'references_column': '', 
        'unique': 'False'
        }, 
    'Sökt antal omgångar': {
        'type': 'VARCHAR', 
        'length': '255', 
        'nullable': 'False', 
        'key': 'None', 
        'auto_increment': 'False', 
        'references_table': '', 
        'references_column': '', 
        'unique': 'False'
        }, 
    'Sökt antal platser per omgång': {
        'type': 'VARCHAR', 
        'length': '255', 
        'nullable': 'False', 
        'key': 'None', 
        'auto_increment': 'False', 
        'references_table': '', 
        'references_column': '', 
        'unique': 'False'
        }, 
    'Sökt antal platser totalt': {
        'type': 'VARCHAR', 
        'length': '255', 
        'nullable': 'False', 
        'key': 'None', 
        'auto_increment': 'False', 
        'references_table': '', 
        'references_column': '', 
        'unique': 'False'
        }, 
    'Diarienummer': {
        'type': 'VARCHAR', 
        'length': '255', 
        'nullable': 'False', 
        'key': 'Primary Key', 
        'auto_increment': 'False', 
        'references_table': '', 
        'references_column': '', 
        'unique': 'True'
        }
    }, 
'TestTable2': {
    'Flera kommuner': {
        'type': 'INTEGER', 
        'length': '255', 
        'nullable': 'False', 
        'key': 'Primary Key', 
        'auto_increment': 'True', 
        'references_table': '', 
        'references_column': '', 
        'unique': 'False'
        }, 
    'Antal kommuner': {
        'type': 'VARCHAR', 
        'length': '255', 
        'nullable': 'False', 
        'key': 'None', 
        'auto_increment': 'False', 
        'references_table': '', 
        'references_column': '', 
        'unique': 'False'
        }, 
    'Län': {
        'type': 'VARCHAR', 
        'length': '255', 
        'nullable': 'False', 
        'key': 'None', 
        'auto_increment': 'False', 
        'references_table': '', 
        'references_column': '', 
        'unique': 'False'
        }
    }
}