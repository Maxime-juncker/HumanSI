import threading




def oui():
    while True:
        print("oui")

def non():
    while True:
        print("non")


t = threading.Thread(target=oui)
t.start()


t2 = threading.Thread(target=non)
t2.start()