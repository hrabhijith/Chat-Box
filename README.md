## Chat Box with emotion detection

The application lets the users to get registered in to the system and login to the public chat session where an individual can chat with others.

The application also analyzes the phrases submitted each time to the session by the user for emotions using IBM tone analyzer API and appends an appropriate emoticon at the end of each message. 

# Installation and reference to execute from local

* This application is full stack and built using Python Flask with SQLAlchmy ORM and few other modules.
* Requires Python 3.6.8 [link to download](https://www.python.org/downloads)
* First run this command from any IDE in Python interpreter(terminal) to download all the required modules - `pip3 install -r requirements.txt`
* Then, run this command to setup database objects - `python database_setup.py`
* Next, run this command and the application starts running and can be viewed in browser at **localhost:1111** - `python main.py`
* Sigup if new user or login to enter the public chat session and start chatting!!
* To see two or more users chatting from same browser/machine use **incognito windows**.