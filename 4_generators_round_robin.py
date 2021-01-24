def gen1(s):
    for i in s:
        yield i


def gen2(n):
    for i in range(n):
        yield i


g1 = gen1('konstantin')
g2 = gen2(3)

tasks = [g1, g2]

while tasks:
    task = tasks.pop(0)

    try:
        res = next(task)
        print(res)
        tasks.append(task)
    except StopIteration:
        pass
