from jug import TaskGenerator

@TaskGenerator
def hello_world():
    with open('hello.txt', 'wt') as out:
        out.write("Hello World\n")


hello_world()
