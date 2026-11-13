marks = {
    "Sajjad" : 40,
    "Ali" : 35,
    "Runu" : 80,
    0: "Harry"
}
print(marks.items())
print(marks.keys())
print(marks.values())
marks.update({"Sajjad" : 99 , "Sunny" : 68})
print(marks)
print(marks.get("Sajjad2")) # prints none
print(marks["Sajjad"]) # returns an error
print(len(marks))