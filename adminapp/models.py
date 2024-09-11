from django.db import models

# Create your models here.
class All_users_model(models.Model):
    User_id = models.AutoField(primary_key = True)
    user_Profile = models.FileField(upload_to = 'images/')
    User_Email = models.EmailField(max_length = 50)
    User_Status = models.CharField(max_length = 10)
    
    class Meta:
        db_table = 'all_users'
        
          
class Efficientnet_model(models.Model):
    User_id = models.AutoField(primary_key = True)
    model_accuracy = models.CharField(max_length = 10)
    executed= models.CharField(max_length = 10, null=True)
    
    class Meta:   
        db_table = 'Efficientnet'
        
        
class Cnn_model(models.Model):
    User_id = models.AutoField(primary_key = True)
    model_accuracy = models.CharField(max_length = 10)
    executed= models.CharField(max_length = 10, null=True)
    
    class Meta:
        db_table = 'Cnn'   
        
        
class Inception_model(models.Model):
    User_id = models.AutoField(primary_key = True)
    model_accuracy = models.CharField(max_length = 10)
    executed= models.CharField(max_length = 10, null=True) 
    
    class Meta:
        db_table = 'Inception'
        
        
        
class Train_test_split_model(models.Model):
    User_id = models.AutoField(primary_key=True)
    training_accuracy = models.CharField(max_length=10, null=True)
    validation_accuracy = models.CharField(max_length=10, null=True)
    testing_accuracy = models.CharField(max_length=10, null=True)
    classes_accuracy = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'Traintestsplit'
        
        
class Comparison_graph(models.Model):
    User_id = models.AutoField(primary_key = True)
    Cnn =models.CharField(max_length = 10, null=True) 
    Efficientnet = models.CharField(max_length = 10, null=True) 
    Inception =models.CharField(max_length = 10, null=True) 
    
    
    class Meta:
        db_table = 'Comparisongraph'        
