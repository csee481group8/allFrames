import os
import json
import SignUp as sgn
from tkinter import *
from tkinter import messagebox

global pwd
#### this auth module needs to be updated if cloud service is used 
# store the same file path used by the sign up function
file_name="user_data.json"

# define a function to check if the login username is stored in json file
# username and password are parameters
# returns False if file does not exist or username not found
# if user name and password are correct, return true.
def auth(username:str,password:str):
    # Load existing user data if the file exists
    try:
        with open(file_name, 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        return False

    # Check if the username already exists in the user data
    for user in users:
        if user['username'] == username:
            # store the password of this user account in variable pwd
            if password == user['password']:
                print(password)
                return True

