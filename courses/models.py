from django.db import models

# Create your modefrom django.db import models


class Course(models.Model):
   name = models.CharField(max_length=80)
   instructor= models.CharField(max_length=100)
   category = models.CharField(max_length=100)
   schedule = models.JSONField(default=dict)
def __str__(self):
        return self.name


class StudentCourse(models.Model):
   student_id = models.IntegerField()
   
   course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='student_courses')
  



   
def __str__(self):
        return f"Student {self.student_id} enrolled in {self.course.name}"
