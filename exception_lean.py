class NoAns(Exception):
    def __init__(self,msg):
        self.msg=msg

def func():
    raise NoAns("no no no")

try:
    func()
except NoAns as e:
    print(e.msg)
