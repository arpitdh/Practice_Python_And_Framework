"""There is a function fibo(N) such that 
fibo(N) = N, N <= 1
              else fibo(N)  = 0,1,1,2.....Nth term 
Write a program that implements fibo(N), taking  N as input and giving the output as mentioned below.
Constraints:
1 ≤ N ≤ 10
"""

def fib(n):
    a,b = 0,1
    print a
    for i in range(n-1):
        a,b = b,a+b
        print a
        
        
if __name__ == "__main__":
    n = int(raw_input())
    if n <= 1:
        print n
    else:
        fib(int(n))
