
import datetime
class chargerLogger: 
    def logWriter(text):
        with open('chargerLog.txt', 'a') as f:
            timestamp=datetime.datetime.now()
            msg=f"{timestamp}::::: {text}"
            f.write(msg)
            print(msg)
            f.close()