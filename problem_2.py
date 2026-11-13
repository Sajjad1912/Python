# c/5 = (f-32)/9 = (k-273)/5

def temp(c) :
    f = (c*(9/5))+32
    return f
c = int(input("Enter temperature in celsius : "))
print("Temperature in fahernheit :",temp(c))