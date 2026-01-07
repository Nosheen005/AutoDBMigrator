# AutoDBMigrator

## How to use the application

The app is simple to use, install openpyxl to a virtual enviroment and run main.py 

### Welcome Screen
After running the file, you will be met with a window to choose which excel database/file you want to use 

If you choose the wrong file, it will allow you to reselect another. You can always go back later to choose again if you change your mind, without needing to restart. 

### Excel Column Selector
Once you have selected a file, just go to the next screen to tell the app where the excel tables are located. You can add as many tables as needed and remove one if you add too many. If you somehow added more tables than it fits on your screen scrolling will be possible 

### Table Editor
After you have filled in the coordinates for your table’s columns and the table names, you can just click next to start modifying the tables to fit your new database model. Just select the table you want to move to in the dropdown, click the column you want to move then click move. Repeat until you are happy then click next to start filling in the details about each column.

### Column Details
Here you choose which table and column you want to work on and then choose the option that suits you for the different details, details such as data type, if it allows nulls or if it is a type of key and similar. Details depending on different values will only show when that condition is met. Such as the referenced table and column can only be selected if you have chosen the column as a foreign key and only shows primary keys to reference

### Script Preview
After finishing you will see a preview of the script to be able to manually change anything if you prefer or you can choose to save the script as a file for later use. You also get options to copy the script, refreshing hence restoring the script if you made any errors.
