from django.db import models
from datetime import date
import re
import bcrypt

class UserManager(models.Manager):
  def registerValidator(self, postData):
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    userswithSameemail = User.objects.filter(email = postData['email'])
    errors = {}
    if len(postData['fname']) == 0:
      errors["fnameReq"] = "First Name is reuqired!"
    elif len(postData['fname']) < 2:
      errors["fnameLen"] = "First Name must be 2 characters long!"
    if len(postData['lname']) == 0:
      errors["lnameReq"] = "Last Name is required!"
    elif len(postData['lname']) < 2:
      errors["lnameLen"] = "Last Name must be 2 characters long!"
    if len(postData['email']) == 0:
      errors["emailReq"] = "Email is reuqired!"
    elif not EMAIL_REGEX.match(postData['email']):
      errors['emailPattern'] = "Email is not valid!"
    elif len(userswithSameemail)>0:
      errors['emailregistered'] = "Email is already registered!"
    if len(postData['pw']) < 8:
      errors['PWlen'] = "Password must be 8 characters long!"
    if postData['pw'] != postData['pwc']:
      errors["pwMatch"] = "Password and confirm PW should match!"
    return errors

  def loginValidator(self, postData):
    errors = {}
    userswithSameemail = User.objects.filter(email = postData['email'])
    if len(postData['email']) == 0:
      errors['reqEmail'] = "Email is required to log in!"
    elif len(userswithSameemail) == 0:
      errors['emailNotFound'] = "This email is not registered yet. Please register first"
    else:
      if not bcrypt.checkpw(postData['pw'].encode(), userswithSameemail[0].password.encode()):
        errors['incorrectPW'] = "Password is incorrect!"
    return errors

class ItemManager(models.Manager):
  def itemValidator(self, postData):
    errors = {}
    # today = str(date.today())
    if len(postData['title']) == 0:
      errors['titleReq'] = "Title is required!"
    if len(postData['category']) == 0:
      errors['categoryReq'] = "Please select category from the options!"
    if len(postData['condition']) == 0:
      errors['conditionReq'] = "Please select condition from the options!"
    if len(postData['price']) == 0:
      errors['priceReq'] = "Price is required! To donate p;ease enter $0!"
    return errors


class User(models.Model):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  password = models.CharField(max_length=255)
  confirm_PW = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)
  objects = UserManager()

class Item(models.Model):
  title = models.CharField(max_length=255)
  description = models.TextField()
  image = models.ImageField(default='default.jpg', upload_to='item_pics')
  category = models.CharField(max_length=255)
  condition = models.CharField(max_length=255)
  price = models.CharField(max_length=255)
  creator = models.ForeignKey(User, related_name = 'item_added', on_delete = models.CASCADE)
  favoritor = models.ManyToManyField(User, related_name = 'item_favorited')
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)
  objects = ItemManager()
