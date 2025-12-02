
import time
import threading

loading=True

def load():
    global loading
    index=1
    start=time.time()
    while loading:

        time.sleep(0.05)
        # update_time=1.1
        
        if loading:
            print(f'{['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'][index % 10]}',end='\r')

            index+=1
    end=time.time()
    print(f'用时:{end-start:.2f}s')
th=None
def start_loading():
    global loading,th
    loading=True
    th=threading.Thread(target=load)
    th.start()
def stop_loading():
    global loading
    loading=False

    if th != None:
        th.join()
    print()

    
