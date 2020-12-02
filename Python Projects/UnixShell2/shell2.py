# shell2.py
"""Volume 3: Unix Shell 2.
<Name>
<Class>
<Date>
"""
import os
from glob import glob
import subprocess

# Problem 3
def grep(target_string, file_pattern):
    """Find all files in the current directory or its subdirectories that
    match the file pattern, then determine which ones contain the target
    string.

    Parameters:
        target_string (str): A string to search for in the files whose names
            match the file_pattern.
        file_pattern (str): Specifies which files to search.
    """
    filelist = glob(file_pattern, recursive=True)
    targetlist = []
    for filename in filelist:
        f = open(filename, 'r')

        if target_string in f.read():
            targetlist.append(filename)
    f.close()
    return targetlist



# Problem 4
def largest_files(n):
    """Return a list of the n largest files in the current directory or its
    subdirectories (from largest to smallest).
    """
    
    fileList = []
    fileSizes = []
    for directory, subdirectories, files in os.walk('.'):
    	for filename in files:
    		
    		fileList.append(os.path.join(directory, filename))
    		fileSizes.append(os.path.getsize(os.path.join(directory, filename)))
    		
    sortedList = [x for y, x in sorted(zip(fileSizes, fileList), reverse=True)]
    finalList = sortedList[:n]
    smallestFile = finalList[-1]
    subprocess.Popen(["wc -l < " + smallestFile + " >> smallest.txt"], shell=True)
    
    return finalList
    
# Problem 6    
def prob6(n = 10):
   """this problem counts to or from n three different ways, and
      returns the resulting lists each integer
   
   Parameters:
       n (int): the integer to count to and down from
   Returns:
       integerCounter (list): list of integers from 0 to the number n
       twoCounter (list): list of integers created by counting down from n by two
       threeCounter (list): list of integers created by counting up to n by 3
   """
   #print what the program is doing
   integerCounter = list()
   twoCounter = list()
   threeCounter = list()
   counter = n
   for i in range(n+1):
       integerCounter.append(i)
       if (i % 2 == 0):
           twoCounter.append(counter - i)
       if (i % 3 == 0):
           threeCounter.append(i)
   #return relevant values
   return integerCounter, twoCounter, threeCounter

"""if __name__ == "__main__":
    print(largest_files(20))"""
    
    
    
    
    
    
