# telegram_manager

## Table of contents
- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [How-To](#how-to)

## Introduction
A simple python program that works with Telegram groups using telethon library.
Functionality:
* Connect to user account
* Read all existing groups
* Create a new group
* Exctract user infromation from groups
* Add users to newly created group

## Prerequisites
#### Python3.6 and above
For windows, download installer from python [official website](https://www.python.org/downloads/windows/) and just click "Next".  
On Linux systems it should be preinstalled.  

#### telethon library
* Open Terminal or Powershell
* Upgrade pip to latest version  
```python -m pip install --upgrade pip```  
* Install library  
```python -m pip install telethon```

## Configuration
There is a configuration file - "config.txt". Parameters in detail:  
* ```api_id``` and ```api_hash```: can be obtained after filling the form at [Telegram Core](https://core.telegram.org/api/obtaining_api_id)  
* ```phone```: your phone number, which was used to register Telegram. An one-time password will be send to it for verification.  
* ```group_name```: group name for the newly created group  
* ```about```: description of for the newly created group  


## How-To
Currently the code is not very flexible, it works linearly and no OOP implemented yet.  
Run program:  
* open Terminal or Powershell and run script  
  ```python main.py```
* if script is run for the 1st time, user will be promted to enter a phone number (same as in config.txt). 
  a verification code will be sent to user's Telegram account, and it needs to be entered in the next promt.
* after verification, script will list available gorups, from where user can choose accounts for the new group.  
* user is be promted to choose group.
* after choosing group, script will list all available accounts, that can be added to the newly created group.
* user is promted to choose account. 
  Example: Enters IDs of chosen users: 0,5,14,2,5,9
* account will be invited to the new group, otherwise exeption will show an error.


