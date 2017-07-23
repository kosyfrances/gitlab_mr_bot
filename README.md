# Gitlab MR Bot
Gitlab MR bot is a slackbot for Gitlab merge requests. All it does is to send you assigned and unassigned merge requests for a project on Gitlab. This was just a random weekend play project :)

### Tech

Gitlab MR bot is written in Python3 and built on [lins05/slackbot](https://github.com/lins05/slackbot) library.

### Collaboration

Want to contribute? Great!

Clone the repository from [GitHub](https://www.github.com)
```
$ git clone https://github.com/kosyfrances/gitlab_mr_bot.git
```

Gitlab MR bot gets its data from [Gitlab API](https://docs.gitlab.com/ee/api/).

### Installation

**Mac Users**

Be sure to have the following installed and setup first.
* Python 3

Next,
* Install [Virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/install.html).
* Create a virtual environment for the project.
    ```
    mkvirtualenv <envname>
    ```

* Use the flag `-p python3` if you also have python 2 installed
    ```
    mkvirtualenv -p python3 <envname>
    ```

* Install requirements in the virtual environment created
    ```
    pip install -r requirements.txt
    ```

* Create a `.env` file and copy the contents of `.env.example` file to it.
* Replace the contents of the file appropriately. `ERRORS_CHANNEL` is the channel or slack user where you want errors to be sent to.

### Development

To start the bot

```
$ python run.py
```

Watch the bot come online on slack in a few seconds. Type `help` to get list of commands avaiable.

To run tests
```
$ nosetests
```
