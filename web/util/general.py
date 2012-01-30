import string, random

def get_random_string(length=5):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(length))
