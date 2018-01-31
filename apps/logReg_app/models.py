from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
from datetime import date, datetime
import datetime
from django.contrib import messages

def validBirthday(birthDay):
    birth_day = datetime.datetime.strptime(str(birthDay), '%Y-%m-%d').date()
    today = date.today()
    if birth_day > today:
        return False
    return True

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors["name"] = "Name should be at least 3 characters"
        if not re.match('^[a-zA-Z ]+$', postData["name"]):
            errors['name_letters'] = "Name should have letters and/or spaces only"
        if len(postData['alias']) < 2:
            errors["alias"] = "Alias should be at least 2 characters"
        if " " in postData['alias']:
            errors['alias_spaces'] = "Alias shouldn't have any spaces"
        if not re.match('^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', postData['email']):
            errors['email'] = "Email should be a valid format (example@example.com), and consist of letters, numbers, _ , or ."
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if " " in postData['password']:
            errors['password_spaces'] = "Password shoudn't have any spaces"
        if postData['password'] != postData['r_password']:
            errors['password_match'] = "Passwords do not match"
        if len(self.filter(email = postData['email'])) > 0:
            errors['email_exist'] = "User with that email already exists"
        if not postData['birth_day']:
            errors['empty_date'] = "Date of Birth shouldn't be empty"
        elif not validBirthday(postData['birth_day']):
            errors['future_date'] = "Date of birth is invalid. It can't be a future date"
        return errors

    def creator(self, postData):
        user = self.create(name = postData['name'], alias = postData['alias'], birth_day = postData['birth_day'], email = postData['email'], password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()))
        return user

    def login_validator(self, postData):
        errors = {}
        users = self.filter(email = postData['email'])
        if len(users) < 1:
            errors['email'] = "Email doesn't exist"
        else: 
            if not bcrypt.checkpw(postData['password'].encode(), users[0].password.encode()):
                errors['password'] = "Password doesn't match"
        return errors

class User(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    email = models.CharField(max_length = 100)
    birth_day = models.DateField(auto_now_add=False, auto_now=False)
    password = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()