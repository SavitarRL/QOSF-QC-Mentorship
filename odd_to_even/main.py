"""
n : integer value that is the positive number to compare in list_n,
list_n : integer list that has odd and even numbers.

Returns the list that contains all even numbers

"""

def odd_to_even(n: int, list_n: list[int]):
    
    for i in range(len(list_n)):
        if  list_n[i]%2 == 1:
            list_n[i] = list_n[i] + 1
    return list_n 

    
    
if __name__ == "__main__":
    B = odd_to_even (n = 31, list_n = [1,2,2,4,5,6,7,11,17,21,22,23] )
    print(B) 
    """
    One possible output is “[2,2,2,4,4,6,8,10,18,20,22,22]” 
    Exist multiple solutions
    """
    
    