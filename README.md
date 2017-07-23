[![Coverage Status](https://coveralls.io/repos/github/kosyfrances/gitlab_mr_bot/badge.svg?branch=master)](https://coveralls.io/github/kosyfrances/gitlab_mr_bot?branch=master) [![Build Status](https://travis-ci.org/kosyfrances/gitlab_mr_bot.svg?branch=master)](https://travis-ci.org/kosyfrances/gitlab_mr_bot)

# Gitlab MR Bot
Gitlab MR bot is a slackbot for Gitlab merge requests. All it does is to send you assigned and unassigned merge requests for a project on Gitlab. This was just a random weekend play project :) and it is completely opensource.

### Tech

Gitlab MR bot is written in Python3 and built on [lins05/slackbot](https://github.com/lins05/slackbot) library.

### Deployment
* Don't forget to star this repo if you have not done so :p
* Fork the repo
* Replace the values in `.env.example` with yours in your environmental variable section of wherever you want to deploy to.

### Collaboration

Want to contribute? Great!

Star this repo :p then fork it. Do stuff and create a pull request. Do not forget to write tests :)

Gitlab MR bot gets its data from [Gitlab API v4](https://docs.gitlab.com/ee/api/).

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
