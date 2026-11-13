def rem(l , word):
    n = []
    for item in l :
        if not (item == word):
            n.append(item.strip(word)) # strip() function remove the word from the string
    return n
    
l = ['Sajjad','Rohan','Sunny','Shubham','an']
print(rem(l,'an'))