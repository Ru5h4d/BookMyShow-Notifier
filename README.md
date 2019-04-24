# BookMyShow-Notifier
Sends an email to the  user when BookMyShow adds a format for a language (checks regularly by time interval specified by the user)

Requirements:
- Email provider should allow the python code to access the account. Can be set up for gmail as guided here.
https://youtu.be/JRCJ6RtE3xU?t=19

Detailed steps:
1. Ask user for BookMyShow link for the movie
2. Extract movie name and ask user for check intervals
3. Start the function in a scheduler (implemented using apsscheduler package)
4. Request file from the link and writes it locally
5. Asks user for prefered language
6. Crops HTML file (saved as txt in 4) accordingly
7. Asks user to select from the available formats
8. Looks for format in the cropped file
9. If found then, it sends an email to specified Email address (imlpemented using email.message) and stops executing
10. If not found, it performs 4-9 again after the interval provided in 2
