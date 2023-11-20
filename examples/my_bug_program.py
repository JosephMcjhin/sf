import time
def get_initial_corpus():
    return ["aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"]

step = 0
start = time.time()
def entrypoint(s):
    global step
    x = 0
    step += 1
    if len(s) > 1:
        i1 = ord(s[-1])
        i2 = ord(s[-2])
        for i in range(0, i1 * i2):
            x += 1

    if len(s) > 2 and s[2] == 'b':
        if len(s) > 3 and s[3] == 'a':
            if len(s) > 4 and s[4] == 'd':
                if len(s) > 5 and s[5] == '!':
                    print(f"Found the bug after {step} loop iterations!")
                    print("time elapsed: {}".format(time.time() - start))
                    exit(0)
