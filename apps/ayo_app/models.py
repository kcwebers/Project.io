from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#-------------------------------------------------------------------------------
#User
#-------------------------------------------------------------------------------

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "Invalid First Name! - Must be 2 characters long"
        if not (postData['first_name'].isalpha()) == True:
            errors['first_name'] = "Invalid First Name! - Can only contain alphabetic characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Invalid Last Name! - Must be 2 characters long"
        if not (postData['last_name'].isalpha()) == True:
            errors['last_name'] = "Invalid Last Name! - Can only contain alphabetic characters"
        if len(postData['username']) < 2:
            errors['username'] = "Invalid Username! - Must be 2 characters long"
        # usernameAlreadyExists = User.objects.filter(username = postData['username']).exists()
        # if (usernameAlreadyExists):
        #     errors['username'] = "Username already exists! Please choose another"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email Address!"
        emailAlreadyExists = User.objects.filter(email = postData['email']).exists()
        if (emailAlreadyExists):
            errors['email'] = "Email already in system"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        if postData['password'] != postData['pwconfirm']:
            errors['confirmpw'] = "Password and Confirm Password must match"
        return errors

    def login_validator(self, postData):
        errors = {}
        loginemailAlreadyExists = User.objects.filter(email = postData['emailLogin']).exists()
        if not (loginemailAlreadyExists):
            errors['loginemail'] = "Failure to login"
        user = User.objects.get(email=postData["emailLogin"])
        pw_to_hash = postData["passwordLogin"]
        if not bcrypt.checkpw(pw_to_hash.encode(), user.password.encode()):
            errors['loginemail'] = "Failure to login"
    
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return f"<User object: FN: {self.first_name} LN: {self.last_name} UN: {self.username} EM: {self.email} PW: {self.password} ID: ({self.id})>"