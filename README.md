# ptoform
 
# In ptoform App, employee can submit Paid time off form to thier supervisor and HR.
 
# Requirement
 
* widget_tweaks
* python 3.8.3
* Django 2.2.17

# How to start?
 
* Download project and start it with an editor(like VS code).
* After that, go terminal command 'pip install -r requirements.txt'. You can download the library which you need to start App.
* Set up mysql and create a database.
* Create a .env file in the same directory as manage.py,
  Please write the contents as follows.

  DATABASESPASSWORD=Your Cleardb Password(You sould generate Password. See bellow how to generate)
  EMAIL=Your Gmail Adress
  PASSWORD=password(You sould generate Password. See bellow how to generate)

* How to generate DATABASESPASSWORD?
You do command like this
$ heroku login
# Get a list of apps you own
$ heroku list

$ heroku addons:create cleardb:ignite --app YourAppName
# About The detailed plan is below
https://elements.heroku.com/addons/cleardb

$ heroku config --app YourAppName | grep CLEARDB
# After this command, you will get the following info.
CLEARDB_DATABASE_URL: mysql://username:yourpassword@hostname/databasename?reconnect=true

# So you should change DATABASES on setting_mysql.py file like this
DATABASES = {
    'default': {
        'ENGINE': 'databasename',
        'NAME': 'putyournameonCLEARDB',
        'USER': 'yourusername',
        'PASSWORD': DATABASESPASSWORD,
        'HOST': 'hostname',
        'PORT': 3306
    }
}

#Also you should add the following code in your .env file.
DATABASESPASSWORD=yourpassword

* How to generate PASSWORD for Gmail?
  Please check the following link.
  https://myaccount.google.com/-> security-> app passwords

  Go to your Google Account.
  Select Security.
  Under "Signing in to Google," select App Passwords. You may need to sign in. If you do n’t have this option, it might be because:
  2-Step Verification is not set up for your account.
  2-Step Verification is only set up for security keys.
  Your account is through work, school, or other organization.
  You turned on Advanced Protection.
  At the bottom, choose Select app and choose the app you using and then Select others and then Generate.
  Follow the instructions to enter the App Password. The App Password is the 16-character code in the yellow bar on your device.
  That is Passowrd.

* How to start App? Go terminal and comand "python manage.py migrate". After that, do command "python manage.py runserver" You can see how App is.
* There are three kinds of users. Employee, Supervisor, HR.
* You can create createsuper user(go terminal and command "python manage.py createsuperuser") and go to http://127.0.0.1:8000/admin/. After that, You can create three kinds of Users.
    
# Author
 
* Akinori Toma
* ignitoma_1031@yahoo.co.jp
