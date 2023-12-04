import os
import json

class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
    
    # Define the json file path, this json file only provides the subscribed user's information
    global file_json_path 
    file_json_path = "user_data.json"
    ## cloud registration data center needed for future development

# sign up funtion with username, password, and email as parameters
# no return value 
def sign_up(username:str,password:str,email:str):
    # Create a User object with the provided information
    new_user = User(username, password, email)
    print(User)

    # Store the user information in a local file
    save_user_info(new_user)

    print("\nSign-up successful! User Information:")
    print(f"Username: {new_user.username}")
    print(f"Password: {new_user.password}")
    print(f"Email: {new_user.email}")

# save user account function with user information list as parameter
# save the new user into the json file
def save_user_info(user):

    # Load existing user data if the file exists
    try:
        with open(file_json_path, 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []

    # Add the new user
    users.append({
        'username': user.username,
        'password': user.password,
        'email': user.email
    })

    # Save the updated user data to the file
    with open(file_json_path, 'w') as file:
        json.dump(users, file, indent=2)