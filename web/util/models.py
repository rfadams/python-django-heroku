from web.accounts.models import Activity

def new_activity(*args, **kwargs):
    activity = Activity()
    activity.new_activity_record(*args, **kwargs)
