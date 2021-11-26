from decouple import config

AUTH_USERS = [int(i) for i in config("AUTH_USERS", default="784148805").split(" ")]
