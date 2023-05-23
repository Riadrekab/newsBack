from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Preference
from django.contrib.auth.signals import user_logged_in
from api.gorgias import addFile, updateFile, queryGorgias
import os
from django.conf import settings
from django.utils import timezone


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name
        )
        # create a profile preference username.pl file
        static = os.path.join(settings.BASE_DIR, 'static')
        user_preference = os.path.join(static, f'{user.username}.pl')
        with open(user_preference, 'w') as f:
            f.write('')


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if not created:
        user.username = profile.username
        user.email = profile.email
        user.first_name = profile.first_name
        user.last_name = profile.last_name
        user.save()

        # check if the username.pl file exists
        static = os.path.join(settings.BASE_DIR, 'static')
        user_preference = os.path.join(static, f'{user.username}.pl')
        if not os.path.exists(user_preference):
            with open(user_preference, 'w') as f:
                f.write('')
        else:
            pass

        current_hour = timezone.now().hour
        current_day = timezone.now().weekday()
        at_work = False
        if profile.work == '1':
            profile_work_from = profile.at_work_from.hour
            profile_work_to = profile.at_work_to.hour
            if profile_work_from < current_hour < profile_work_to:
                at_work = True
        else:
            at_work = False

        # check if the user has a preference
        categories = []
        if profile.preferred_topics.exists():
            # get all the preferred topics
            preferred_topics = profile.preferred_topics.all()
            # get the categories of the preferred topics
            for topic in preferred_topics:
                categories.append(topic.category.name)
            # remove duplicates
            categories = list(set(categories))

        # if user has set a preference
        gorgias_preference = ":- dynamic all_time/0, at_work/0, weekend/0.\n"
        if profile.preference_set.all().exists():
            # get the preference
            preferences = profile.preference_set.all()
            list_preferences = [preference.category.name for preference in preferences]
            rules = {}
            for i, pref in enumerate(list_preferences):
                rules[f'r{i + 1}'] = pref

            rule_actions = {}
            for i, pref in enumerate(list_preferences):
                rule_name = f'r{i + 1}'
                corresponding = preferences.get(category__name=pref)
                if corresponding.see_at_work is True and corresponding.see_at_weekend is False:
                    rule_actions[rule_name] = 'at_work'
                elif corresponding.see_at_weekend is True and corresponding.see_at_work is False:
                    rule_actions[rule_name] = 'weekend'
                elif corresponding.see_at_weekend is True and corresponding.see_at_work is True:
                    rule_actions[rule_name] = 'all_time'

            # update the gorgias_preference string
            for rule, action in rule_actions.items():
                gorgias_preference += f'rule({rule}, {rules[rule].lower()}, []) :- {action}.\n'

            # generate the prefer rule for every combination of preferences every rule must have a prefer rule if we have 2 rules we have 2 prefer rules example rule 1 is prefered over rule 2 and rule 2 is prefered over rule 1
            count = 1
            for i in range(1, len(rules) + 1):
                for j in range(1, len(rules) + 1):
                    if i != j:
                        gorgias_preference += f'rule(p{count}, prefer(r{i}, r{j}), []).\n'
                        count += 1

            # generate complement rules for every rule
            for i in range(1, len(rules) + 1):
                for j in range(1, len(rules) + 1):
                    if i != j:
                        right = f'r{i}'
                        left = f'r{j}'
                        gorgias_preference += f'complement({rules[right].lower()}, {rules[left].lower()}).\n'

            # add the gorgias_preference to the username.pl file
            with open(user_preference, 'w') as f:
                f.write(gorgias_preference)

            # add the gorgias_preference to the gorgias server
            status = addFile(user_preference, "newsfilter", "gorgias")
            if status != 200:
                # update the gorgias_preference
                updateFile(user_preference, "newsfilter", "gorgias")

            topic_to_show = []
            facts = ["all_time"]
            if at_work and current_day < 5:
                facts.append('at_work')
            if current_day > 5:
                facts.append('weekend')

            for preference in preferences:
                res = queryGorgias(facts, preference.category.name.lower(), f"newsfilter/{user.username}")
                if res["hasResult"] is True:
                    topic_to_show.append(preference.category.name)
            print(topic_to_show)


def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()


def updatePreference(sender, instance, **kwargs):
    profile = instance.profile
    profile.save()


def upload_profile_preference(sender, instance, created, **kwargs):
    if created:
        profile = instance
        default_preference = os.path.join(settings.BASE_DIR, 'static', 'default_preference.json')
        profile_preference = os.path.join(settings.BASE_DIR, 'static', 'profile_preference.json')
        with open(default_preference, 'r') as f:
            data = f.read()
        with open(profile_preference, 'w') as f:
            f.write(data)


def connect_signal():
    post_save.connect(updateUser, sender=Profile)
    post_save.connect(createProfile, sender=User)
    post_save.connect(updatePreference, sender=Preference)
    post_delete.connect(deleteUser, sender=Profile)
