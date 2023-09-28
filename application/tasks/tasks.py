class MyException(BaseException):
    pass
def hello_task(who='world'):
    print(f'Hello {who}')
    raise MyException('Quebrou')