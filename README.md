# Hirebeat_User_Account_Management

HireBeat is an advanced candidate sourcing and applicant tracking system that seamlessly accelerates recruitment processes. 
This project encompasses both User Management and Account Management functionalities.

##Install and Run Locally
The following steps assume a foundational understanding of Django's concepts, and make sure you have installed python3, pip in your computer.
Then git clone the repo.

1. Set up virtual environment:
   1. `python3 -m venv myenv`(create virtual environment)
   2. `source myenv/bin/activate`(open virtual environment)
   3. `pip install django`(install django)
   4. `pip install django-utils-six`(install necessary package)

2. Run website in localhost:  
`python manage.py runserver`

## Key functions and features:
The whole project have User_Management and Account_Management two parts. 
The following will provide an in-depth exploration of the main functionalities within these two apps.


###User_Management: 

The "User_Management" app serves as a platform to facilitate user registration, login, profile modification, 
and personal information submission and display functionalities.   

####1. Login: 
The User_Management app's model is built upon Django's official User class, with additional fields including `is_active`, `groups`, 
and `user_permission` to enhance the security of user logins.  
The login functionality is implemented through the `CustomLoginView` class, which inherits from Django's built-in LoginView, and renders the login template at `'login.html'`. 
The `CustomLoginView` class is responsible for handling user authentication and managing the login process.
It also checks if the user's email has an associated invitation and, if so, handles account and group assignments.
If user forget password, login page also have `Forget Password` link help user reset password

####2. Register:
1. Register function:  
The `RegisterPage` class in the User_Management app provides user registration functionality. 
It is implemented using Django's `FormView` class and uses the `UserCreationForm` as the form class to collect user registration data. 
The class is responsible for rendering the registration template located at `'signup.html'`.
Upon successful form submission, the `form_valid` method is triggered. It saves the user object with `is_active` set to False.
It then generates an email confirmation token using Django's default token generator. An activation email is composed, including a link with the token, and sent to the user's email address using the `send_mail` function. 
Then an email will be sent to user and a successful message will be displayed in the framework.

2. Activate Account function:  
The ActivateAccount class is responsible for activating user accounts after they have clicked on the activation link sent to their email. 
This User will automatically be assigned as an admin role, indicate this user can have all permission. 

####3. Display and Update user information
These function is included in `UserSettingView` class, which allowing users to update their personal information, change their email address, and modify their account password.
and it is render in `'user_setting.html'`.
1. Updating Personal Information:   
Users can modify their first name and last name through the user_info_form. Upon successful validation, the updated information is saved, and users are redirected to the same settings page with a success message.
2. Changing Email Address:  
The update_email_form provides a means for users to change their email address. After submitting the form, a verification code is generated and sent to the new email address for confirmation. 
The verification code is stored in the session for later use in the email verification process. This part implement in `VerifyCodeView` class.
3. Modifying Password:   
Users can also change their account password using the update_password_form. The form requires users to provide their old password and a new password. If the old password is verified successfully, the new password is checked for complexity requirements and matched for confirmation. Upon a successful password change, 
users are prompted to keep their new password secure and are automatically logged out for security reasons.

##TechStack

