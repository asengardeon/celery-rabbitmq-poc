class MyException(BaseException):
    pass
def hello_task(who='world'):
    print(f'Received {who}')
    if who != 'Kombu':
        raise MyException('Quebrou pois não é Kombu')
    else:
        print(f'Hello {who}')
