#fifteen_secs.py
import time

def fifteen_secs():
    """Runs for about 15 seconds and outputs "Success!"
    """
    start = time.time()
    total = 0
    #loop until the time is reached, give or take a few seconds
    while(total < 15): 
        end = time.time()
        #calculate the new total time
        total = end - start
        
    #print success after the loop exits
    print("Success!")
     
if __name__ == "__main__":
    fifteen_secs()
