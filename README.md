# Hirebeat_User_Account_Management

HireBeat is an advanced candidate sourcing and applicant tracking system that seamlessly accelerates recruitment processes. 
This project encompasses both User Management and Account Management functionalities.

## Install and Run Locally
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


### User_Management: 

The "User_Management" app serves as a platform to facilitate user registration, login, profile modification, 
and personal information submission and display functionalities.   

#### 1. Login: 
The User_Management app's model is built upon Django's official User class, with additional fields including `is_active`, `groups`, 
and `user_permission` to enhance the security of user logins.  
The login functionality is implemented through the `CustomLoginView` class, which inherits from Django's built-in LoginView, and renders the login template at `'login.html'`. 
The `CustomLoginView` class is responsible for handling user authentication and managing the login process.
It also checks if the user's email has an associated invitation and, if so, handles account and group assignments.
If user forget password, login page also have `Forget Password` link help user reset password

#### 2. Register:
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

#### 3. Display and Update user information
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


### Account_Management:

The `Account_Management` app serves as a platform to facilitate account, deleting account, manage new users(invite, deactivate, activate), account modification, 
and account information submission and display functionalities. The `Account_Management` app's model encompasses four essential classes: `Account`, `Role`, `TeamInvitation`, and `AccountUserRelation`.
The `Account` class serves as the model that gathers and holds all pertinent company information for display by the company owner.
The `Role` class defines and describes a user's role or position within the company.
The `TeamInvitation` class facilitates the linkage between the database, accounts, and users, primarily employed for managing and inviting users to the system. 
Lastly, the `AccountUserRelation` class offers a valuable method for establishing and checking the associations between user accounts and the corresponding company accounts.

#### 1. Delete Account:
Delete account will deactivate all users who under an specfic account and the account itself. This feature is render in `delete_account`

#### 2. Delete/activate User:
Delete/activate user will deactivate/activate specific user. Simply set `user.is_active = True/False`

#### 3. Add New User:
This feature is render in `AddUserView` and `RegisterWithInvitationView` classes. Only user in Hiring Managers or Admin Group have the right to add new users. This feature comprises two distinct aspects: inviting users by HR or admin and user registration.

1. invite user(`AddUserView`)：  
After HR or admin fill in the new user's Role name, Role type and email, new user will receive an email include a special link to register. 
In this class's `post` method, a TeamInvitation is created, including email, role, and token, then saved in the database, which will help new user's registration.

2. register with invitation(`RegisterWithInvitationView`):  
The `RegisterWithInvitationView` class handles user registration with an invitation token. It uses the `register_with_invitation.html` template. 
In the get method, the token is decoded and validated against a TeamInvitation entry. If valid, a user creation form is rendered. 
The post method checks the validity of the registration form. If valid, a new user is created and associated with the provided email, username, and password. 
The user is assigned to a group based on the role from the invitation, and an AccountUserRelation is established.

#### 4. Account Setting:
Only Admin and HireManger can access this page.
It uses `edit_account.html`. In get() function, it render account, org_form, user_info_form, user_roles, company. 
the create_or_update_employer_info() function will create or update company logo, video, industry, email, location, size, website, summary, linkedin, facebook, twitter. In the Account Setting page, if the information already fill in before, the blank will be automaticlly fill in, and ther user just need to modify specfic information.

image & video are uploaded to the firebase and the urls are used for display.  `<img src=url >`

#### 5. ConfigureView:
Displaying all user-operable features, the `User` section includes the ability for HR and admin users to `Manage/Invite` other users. 
This right is exclusively granted to HR and admin roles.

#### 6. OrganizationView:
Instead of editing the account information, it displays account information. `get()` provide important information for furher uses.

#### 7. ManageUserView:



## TechStack
Our HireBeat website is built on the following tech stack:
1. **Backend Development**: Utilizing the Django framework to establish a robust backend logic and manage the database.
2. **Frontend Design**: Employing HTML, CSS, and JavaScript for frontend design and development, ensuring a user-friendly interface and interactive experience. 
The website template is based on `https://elements.envato.com/learning-dashboard-template-DLH2S6X`.
3. **Database**: Using SQLite for development and testing.
4. **User Authentication**: Leveraging Django's built-in user authentication system to ensure secure user login and registration.
5. **Cloud Storage**: Integrating Firebase cloud storage to enable users to upload and manage multimedia resources such as images and videos.
6. **Third-party Libraries**: Utilizing Django's built-in libraries along with other third-party libraries to provide rich functionality, including `form validation`, `email sending`, and `permission management`.
7. **Version Control**: Employing Git for version control, facilitating team collaboration and code management.  

Our chosen tech stack is designed to offer users an efficient, secure, and seamless recruiting experience.