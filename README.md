# lab1
Student Name:AsiahZibrila
id: 30162026
This website is a platform for bookreviews, users are able to register and login to leave reviews for any book 
and also find reviews left by other users. The app name is asiabooks.
Key Functionalities :
Once a user is logged in, page shows users userenam; "logged in as:username". User is also able to logout. 
User can search by the author, title or isbn of a particular book, they can search by just a part of the isbn,title or isn, a search results will display.
User can click on any book in the search results to open th ook page.
User can rate a book and add a text comment. They can also see reviews from others.Users can only add rate and review a book once.
The API ccess button is also active and a user can use the url to find a book, with a particular isbn, this returs the details about the book including the rate count.
FILES: app.py is the factory file ,The import.py contains the codes for the import from csv and connection to database. In the models.py file three tables were created , Persons table(same as users)
,Books table and review table.auth.py includes the codes for registration, login and logout. static folder containts the html files for the webpage designs. api.py imports google API functionality.
Templates folder also has the html diles for the page section designs. 
