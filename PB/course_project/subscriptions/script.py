from subscriptions.models import UserSub

all_usersubs = UserSub.objects.all()

for user in all_usersubs:
    user.renew_required()