import threading
import time

class Waiting(threading.Thread):

    def __init__(self):
        super().__init__()
        self.state = 0
        self.animation = [".  ",".. ","..."]
        self.percent = 0
        self.daemon = True
        self.active = False
        

    def start(self):
        self.active = True
        super().start()
        
    def update(self,percent):
        self.percent = percent
            
    def stop(self):
        self.state = 0
        self.active = False

    def run(self):
        while self.active:
            print(str(self.percent)[:4]+"% "+self.animation[self.state % len(self.animation)],end="\r")
            self.state += 1
            time.sleep(0.4)
            
    def stop(self):
        self.active = False
