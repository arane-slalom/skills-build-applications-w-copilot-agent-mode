from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Ensure the database is connected
        if not settings.DATABASES['default']['ENGINE'] == 'djongo':
            self.stdout.write(self.style.ERROR('Database engine is not set to djongo.'))
            return

        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activity.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create users
        users = [
            User(email='thundergod@mhigh.edu', name='Thor', age=30),
            User(email='metalgeek@mhigh.edu', name='Tony Stark', age=45),
            User(email='zerocool@mhigh.edu', name='Steve Rogers', age=100),
            User(email='crashoverride@hmhigh.edu', name='Natasha Romanoff', age=35),
            User(email='sleeptoken@mhigh.edu', name='Bruce Banner', age=40),
        ]
        for user in users:
            user.save()

        # Create teams
        team1 = Team(name='Blue Team', members=[user.email for user in users[:3]])
        team2 = Team(name='Gold Team', members=[user.email for user in users[3:]])
        team1.save()
        team2.save()

        # Create activities
        activities = [
            Activity(user=users[0], description='Cycling', timestamp=now()),
            Activity(user=users[1], description='Crossfit', timestamp=now()),
            Activity(user=users[2], description='Running', timestamp=now()),
            Activity(user=users[3], description='Strength Training', timestamp=now()),
            Activity(user=users[4], description='Swimming', timestamp=now()),
        ]
        for activity in activities:
            activity.save()

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(team=team1, score=300),
            Leaderboard(team=team2, score=250),
        ]
        for entry in leaderboard_entries:
            entry.save()

        # Create workouts
        workouts = [
            Workout(user=users[0], type='Cycling', duration=60),
            Workout(user=users[1], type='Crossfit', duration=90),
            Workout(user=users[2], type='Running', duration=120),
            Workout(user=users[3], type='Strength Training', duration=45),
            Workout(user=users[4], type='Swimming', duration=75),
        ]
        for workout in workouts:
            workout.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
