# coding: utf-8
from django.core.management import BaseCommand
from datetime import datetime, timezone
from tasks.models import TodoItem
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = u"Display top users by tasks"

    def add_arguments(self, parser):
        parser.add_argument('--number_users', dest='num_top_users', type=int, default=25)

    def handle(self, *args, **options):
        all_users = []
        for u in User.objects.all():
            all_users.append(u)
        #sort users by number of tasks in descending order 
        for index in range(1, len(all_users)):
            top = index
            while top > 0 and (all_users[top-1].tasks.count() < all_users[top].tasks.count()):
                all_users[top - 1], all_users[top] = all_users[top], all_users[top - 1]
                top -= 1  
        #print(all_users)    
        select_users = []
        count = options['num_top_users']
        #select number 'num_top_users' of top users by tasks 
        select_users = all_users[0:count]

        #counting all tasks and of all users 
        all_tasks = 0
        for user in all_users:
            all_tasks += user.tasks.filter(is_completed=True).count()
        print(all_tasks)

        #counting all tasks of fith user of top users with maximum numbers of tasks
        print(all_users[4].tasks.count())

        count_users = 0   
        #counting users which have incomplete task less than 20
        for user in all_users:
            if user.tasks.filter(is_completed=False).count() < 20:
                count_users += 1
        print(count_users)    

        #sort users by number of incomplite tasks in descending order 
        for index in range(1, len(all_users)):
            top = index
            while top > 0 and (all_users[top-1].tasks.filter(is_completed=False).count() < all_users[top].tasks.filter(is_completed=False).count()):
                all_users[top - 1], all_users[top] = all_users[top], all_users[top - 1]
                top -= 1
        print (all_users[1])
            