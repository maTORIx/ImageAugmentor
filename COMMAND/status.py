import json
import datetime

class Status(object):
    def __init__(self, path=None, message="processing", progress=0, max_progress=100):
        self.path = path
        self.message = message
        self.progress = progress
        self.max_progress = max_progress
        self.last_write = datetime.datetime.now()
        self._write()
    
    def _write(self):
        st = {"message": self.message, "progress": self.progress, "max_progress": self.max_progress}
        self.last_write = datetime.datetime.now()
        
        if self.path == None:
            for key in st:
                print("{}:{}".format(key, st[key]))
        else:
            with open(self.path, "w+") as f:
                f.write(json.dumps(st, indent=2))
    
    def write(self):
        if (datetime.datetime.now() - self.last_write).seconds < STATUS_WRITE_SPAN_SEC:
            return
        self._write()
    
    def update_msg(self, message):
        self.message = message
        self._write()
    
    def add_progress(self, num):
        self.progress += num
        self.write()

    def finish(self):
        self.progress = self.max_progress
        self.message = "finished"
        self._write()
