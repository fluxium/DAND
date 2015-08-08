'''
Programming background in Python.

The first exercise allows you to assess your ability to program in Python.
As a data analyst, you will spend much of your time writing code and
programs to work with data or to build mathematical, statistical, or
machine learning models to find insights from data.

Complete this function that modifies a list of integers.

1)  For numbers that are multiples of three replace the integer with the string "Fizz".

2)  For numbers that are multiples of five replace the integer with the string "Buzz".

3)  For numbers that are multiples of both three AND five replace the integer
    with the string "FizzBuzz"

Your function should take in a list of integers as input.
Your function should not modify the input list.
Your function should return an updated list with integers and strings.
'''

def fizzbuzz(intList):
    '''
    Your fizzbuzz function. The grader will run `fizzbuzz(intList)` to check if your
    function returns the correct output.
    
    intList: list containing integers

    Make sure you write the script so that your algorithm is part of the
    function; you do not need to call the function yourself.
    '''    
    tempInts = intList[:]
    
    for index, num in enumerate(tempInts):
        #print(index)
        #print(num)
        if (num > 0):
            if (num % 3 == 0 and num % 5  == 0):
                tempInts[index] = 'FizzBuzz'
            elif (num % 3 == 0):
                tempInts[index] = 'Fizz'
            elif (num % 5 == 0):
                 tempInts[index] = 'Buzz'
    
    return tempInts