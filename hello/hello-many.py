from jug import TaskGenerator

@TaskGenerator
def hello(name):
    from time import sleep
    sleep(6) # Pretend this is taking a long time
    with open(f'hello-{name}.txt', 'wt') as out:
        out.write(f"Hello {name}\n")


for name in [
        'Shaojun',
        'Yiqian',
        'Svetlana',
        'Celio',
        'Chengkai',
        'Hui']:
    hello(name)
