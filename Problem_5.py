def patteern(n):
    if n == 0 :
        return 1
    print("*" * n)
    patteern(n-1)
    
n = int(input("Enter number : "))
patteern(n)