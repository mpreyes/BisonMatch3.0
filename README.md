
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


## Setting up Paypal

Here are some steps to take to set up Paypal on your localhost.

1. Login to the Paypal's sandbox part of the site [here](https://developer.paypal.com/developer/accounts/)
2. Click on **My Apps & Credentials** on the lefthand side under **Dashboard**.
  * Click onto the BisonMatch App
3. Click **Add Webhook**. This is where Paypal will attempt to make the POST to once it completes the transaction.
  * Add the full address of the link to send the POST request to. Something like https://localhost:8000/bisonMatch/thanks

Now Paypal should be able to send a POST to the correct place. Next we have to create the button for the website, and this does have
to be specific in order for it to work.

1. Login to the regula Paypal site [here](https://www.paypal.com/us/home)
2. In the main navigation bar hover over **Tools**, then select **All Tools** in the dropdown.
3. Scroll down and select **Paypal Buttons**
4. Select the **Buy Now** button.
5. Fill in the *Item Name* and *Price* then scroll down and select *Step 3*.
6. Check the boxes **Take customers to this URL when they cancel** and **Take customers to this URL when they finish checkout** and add the appropriate
locations.
7. Check the **Advance Variables** box and type in:

```
notify_url=https://myapp.com/url_to_notify
```

8. Create the button and add the code.


# Notes:

Use python3 to avoid confusion.
Digital Ocean Django droplet for server, Talk to Becky Tallon to point domain name "bisonmatch.info" to server ip address and use masking.


## TODO: Version 4 Changes & Improvements:

Fix app so it can be taken off of debug mode (pictures)
Add column to db to keep track of results sent
Improve payment!
Fix form inputs to protect from sql injection while allowing all characters. 
Form inputs accept emoji’s
Get system to make calls to DB in batches when generating matches and sending emails
SECURITY (HTTPS)
New Questions
Add extra email to send only to people who have not paid as a final reminder the last day of sales.
Way to download your results
Add capacity to send more emails
Get other people to work the bisonmatch table

Dates to be live (the entire week before and week of Feb 14) Send ALL results Feb 13



