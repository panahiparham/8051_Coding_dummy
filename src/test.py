import inspect

def f1():
    if inspect.stack()[1][3] == 'main':
        print('running f1')


def f2():
    if inspect.stack()[1][3] == 'main':
        print('running f2') 
    f1()



def main():
    f2()

main()