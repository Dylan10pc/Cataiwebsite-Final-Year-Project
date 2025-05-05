from django.db import models

# Create your models here.

#model for the cat image to store information about the image
class catimage(models.Model):
    #image field to store the uploaded image
    image = models.ImageField(upload_to="uploads/")
    #timestamp field to store the time the image was uploaded
    uploadedwhen = models.DateTimeField(auto_now_add=True)
    
    #fields to store the predicted breed, confidence and facts
    predictedbreed1 = models.CharField(max_length=100, blank=True)
    confidence = models.FloatField(default=0)
    facts = models.JSONField(default=dict)
    