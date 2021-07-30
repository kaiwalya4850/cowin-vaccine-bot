# Cowin Bot

My own bot on telegram is live by this username: @CoWINchecker_bot (inactive now!)


A telegram bot that shows a number of available vaccines in vaccination centers near you. 

This takes Age and Postal Code as input from the user. Based on this, you'll get all the vaccination center names and available vaccines. 

Sometimes, there are some issues with the API they've provided so, it stops working.

This is how the output looks like:

``
Here are all vaccination centers and vaccine count corresponding to the postal code you mentioned: [{'Maa Bharti School 18 To45': 0}, {'HCG ONCOLOGY SUNFARMA ROAD': 0}, {'Sir Sayajirao Nagargruh18to45': 0}, {'HCG ONCOLOGY SUNFARMA ROAD': 0}, {'Sir Sayajirao Nagargruh18to45': 0}, 'No available slots on: 07-05-2021', 'No available slots on: 08-05-2021', 'No available slots on: 09-05-2021', 'No available slots on: 10-05-2021', 'No available slots on: 11-05-2021']
``


## Usage
Open Telegram, go to Botfather, and get a token.

Replace this token with "TOKEN" in the code.

Run it like
```python
python bot.py
```
You can even study the time at which the slots open in your city and book according to pattern. To get the results run:
```python
python nodb.py
```
To keep all track on Google Firestore, run:
(Make sure you add .json file from Firestore)
```python
python checker.py
```
## Future updates
Deployment on Heroku

Until then... Stay home, stay safe!
