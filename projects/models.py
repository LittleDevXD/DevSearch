from django.db import models
from users.models import Profile
import uuid

# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title

    @property
    def reviewers(self):
        query_set = self.review_set.all().values_list('owner__id', flat=True)
        return query_set

    # calculate vote total and vote ratio
    @property 
    def get_vote_count(self):
        reviews = self.review_set.all()
        up_vote = reviews.filter(value='up').count()
        total_vote = reviews.count()

        # Zero Division Error
        if total_vote:
            ratio = (up_vote / total_vote) * 100
            self.vote_ratio = int(ratio)
            self.vote_total = total_vote
            self.save()

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']      # -created to display newest 

class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up vote'),
        ('down', 'Down vote')
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name