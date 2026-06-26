from config import LOG_SEPARATOR


def banner(title):

    print(LOG_SEPARATOR)
    print(title)
    print(LOG_SEPARATOR)


def item(key, value):

    print(f"{key:<15}: {value}")