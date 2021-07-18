import time
from loadingindicator.LoadingBar import LoadingBar

def main():
    bar = LoadingBar(100)
    for i in range(0, 101, 2):
        bar.set_progress(i)
        bar.draw()
        time.sleep(0.05)

if __name__=="__main__":
    main()
