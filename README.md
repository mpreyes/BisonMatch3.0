## Bison Match 3.0


1. Install django version 2.0.2

2. Install the mysqlclient:

    `pip3 install mysqlclient`

3. To run the development server:

    `python3 manage.py runserver`



4. For the Database:
    1. Create a new Database called BisonMatch3
    2. In your migrations folder, you might have some files of the form 000*_initial.py. Delete those files before moving on. (Not the __init__.py file!)
    3. `python3 manage.py makemigrations`
    4. `python3 manage.py migrate`
    5. Success! you now have our database schema in your test database.


Notes:

Use python3 to avoid confusion.



