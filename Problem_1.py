def greatest(a,b,c) :
    if a>b and a>c :
        return a
    elif b>a and b>c :
        return b
    if c>a and c>b :
        return c
    
n1 = int(input("Enter a number : "))
n2 = int(input("Enter a number : "))
n3 = int(input("Enter a number : "))
print("The greatest number is : " , greatest(n1,n2,n3))