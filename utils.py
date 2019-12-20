from datetime import datetime


def timenow():
    """Console log current time.
    """
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return now.strftime("[%H:%M:%S] ")
