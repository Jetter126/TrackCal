# TrackCal

<trackcalapp.herokuapp.com>

TrackCal is a web application that helps people track their calories and achieve their weight gain or weight loss goals.
It includes:

* A user system that lets users sign up, log in and track their progress.
* A home page that displays quick tips related to calories and weight.
* A calculator that allows the user to calculate their basal metabolic rate (BMR), which is the number of calories their body burns just by existing and carrying out its basic functions like breathing and thinking.
* A calorie tracker that lets the user set a calorie goal based on their weight loss or weight gain goal, as well as log the number of calories they consume on a daily basis.
* An information page that provides the user with further information regarding the science behind calories, weight gain and weight loss.

## Video Demo:

https://www.youtube.com/watch?v=xUk4zFCMeCU

## Description:

TrackCal's back-end runs on Python and Flask, a micro web framework written in Python. The databases are created and handled by SQLAlchemy, an SQL toolkit, while the application's front-end is written in HTML and CSS, with most of the styling being done with the help of Bootstrap. The following are the different files and pages of this project:

#### app.py

app.py contains the back-end of the application. After importing the required libraries, the Flask app is initialized and configured here. After that, SQLAlchemy is configured and the models stored in calories.db are created. Finally, the file contains 7 functions that are called when the application redirects to each function's respective route.

#### calories.db

calories.db contains all the data that TrackCal handles. This is in the form of 2 tables: Users and Tracker. Users stores each user's username, email, a hashed form of their password, their calorie goal and the date the account was created. Tracker stores a day, month and year as well as how many calories a user ate on that given day. The two tables are linked by the primary key in the Users table, id, which appears as a foreign key in the Tracker table, user_id.

#### layout.html

layout.html contains the skeleton of the application which is extended by the other HTML files. It contains a navbar that allows the user to sign up, log in or log out, as well as access the home, calculator, calorie tracker and information pages.

#### index.html

index.html displays the home page. If the user is logged in, the navbar displays the logo, as well as links to the other pages. This navbar is also present on the other pages. The home page is divided into three sections: the carousel, information and YouTube videos. The carousel displays tips and facts related to calories, weight gain and weight loss, while the information section contains information related to the same as well as links to the other pages. The embedded YouTube videos further explain the science behind calories and weight.

If the user hasn't logged in, the home page displays the logo and options to either log in or sign up.

#### signup.html

The sign up page allows users to create an account. The four input fields let the user enter their username, email ID, password and password confirmation, and the submit button passes this information to app.py. If the username and email are unique and the password is valid (at least 8 characters in length and contains at least 1 digit) the information is stored in the Users table. A red alert is displayed if there are any errors while signing up.

If the user already has an account, they are given the option to log in.

#### login.html

The log in page allows users to log in if they have an account. There are two input fields for username and password, as well as a submit button to submit the form. This information is sent to app.py, where it is checked against the data in the Users table. If the username and password are valid and match, a new session is created and the user is redirected to the home page. A red alert is displayed if there are any errors while logging in.

If the user doesn't have an account, they are given the option to sign up.

#### bmrcalculator.html

bmrcalculator.html displays a calculator that allows the user to calculate their basal metabolic rate (BMR), which is the number of calories their body burns just by existing and carrying out its basic functions like breathing and thinking. The user can input their age (from 15 to 80), weight, height and gender, and the submit button passes this information to app.py, where the user's BMR is calculated. This value is then displayed. A red alert is displayed if there are any errors.

#### calories.html

calories.html displays a page with three sections. The first section contains instructions on how the user can track their calories. 

The next section contains a form where the user can find their calorie goal based on their weight loss or weight gain goals. After providing their BMR, whether they want to lose or gain weight and their target weight change per week, the submit button sends the information to app.py. After the goal is calculated, it is displayed on every page of the application and is stored in the Users table. A red alert is displayed if there are any errors.

The third section allows the user to log their calories. The form has fields for the date and number of calories, as well as buttons to add, remove or view calories. The changes are recorded in the Tracker table and a progress bar is displayed with the calorie intake.
A red alert is displayed if there are any errors.

#### information.html

information.html is a static page that displays information about the science behind calories, weight loss and weight gain.

#### donate.html

donate.html allows the user to donate through a PayPal link.