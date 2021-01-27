# my-shop
GUI APP written in Python using tkinter and sqlite.
Application is secured for inserting incorrect data.
All methods, modules and classes have proper docstrings.


## Features
- create new account
- login as admin or user (the appropriate window will open based on permissions)
- User: search and order products (if available in stock), edit account
- Admin: CRUD operations for customers, products and orders

## Handy solutions
- All tables are interactive, each row can be selected - based on selection other tables or inputs handle specific event
- Example: When admin clicks on specific order, appropriate user and products will be listed in tables,
it works identically the other way round so there is no need to manually write user's or product's details

# example acc:

- Admin perms

login: admin,
passsword: admin123

- User perms

login: wojtekkk,
password: mojehaslo123

## preview

### order panel
<img src="https://user-images.githubusercontent.com/64193740/105970720-f872ef00-6089-11eb-98c2-6f3db64ec405.png" width=800>


### users panel
<img src="https://user-images.githubusercontent.com/64193740/105970776-06287480-608a-11eb-940f-ed337c57e893.png" width=800>



