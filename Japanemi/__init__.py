import logging
from logging import handlers
from decouple import config


# DEBUG
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING,
                    handlers=[
                        handlers.RotatingFileHandler(
                            filename="./logs/sayu.log",
                            maxBytes=3145728,
                            backupCount=1
                        ),
                        logging.StreamHandler()
                    ]
                    )
sayulog = logging.getLogger("Japanemi")


AUTH_USERS = [int(i) for i in config("AUTH_USERS", default="784148805").split(" ")]
