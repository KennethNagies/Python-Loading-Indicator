import time
from loadingindicator.LoadingBar import LoadingBar

def main():
    bar = LoadingBar(500, "Some Crazy Long Title That Will Allow Us To Force Truncation By Changing The Width Of The Terminal Before Running This Test")
    for i in range(0, 501, 2):
        bar.set_progress(i)
        bar.draw()
        time.sleep(0.01)
    bar.set_title("Done Testing!")
    bar.draw()

if __name__=="__main__":
    main()
