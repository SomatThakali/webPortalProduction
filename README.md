# webPortalProduction

We can use the file as a manual for Burke on how they use the website once it is done. 

How to create a super user (admin) account :
1_ open cmd and cd into the dir where the repo is installed.
2_ in the terminal type : python manage.py createsuperuser
3_ chose a username and password and click enter.
4_ go to the log-in page and enter the created credentials to log in as admin

How to create patient and therapist accounts:
1_ create a group and call it "patient" or "therapist" ( mind the lower case )
2_ when creating a new user add it to either group according to its role 
3_ create a username and password for the new user
