

print("problem 9")

for row in range(10):

    for space in range(row):
        print(end = "  ")
    for column in range(10-row):
        print(column, end = " ")

    print()

print("problem 10")

for row in range(1,10):
    for column in range(1,10):
        result = row*column
        if row*column < 10:
            print(" ", end = "")

        print(result, end = " ")

    print()

for xilon in range(3):
    print()

print("problem 11")

for i in range(10):
    for j in range (10-i):
        print(" ", end = " ")
    for j in range(1,i+1):
        print(j, end=" ")
    for j in range(i - 1, 0, -1):
        print(j, end=" ")
    print()

for row in range(10):

    for space in range(row):
        print(end = "  ")
    for column in range(10-row):
        print(column, end = " ")

    print()

print("problem 13")

for i in range(10):
    for j in range (10-i):
        print(" ", end = " ")
    for j in range(1,i+1):
        print(j, end=" ")
    for j in range(i - 1, 0, -1):
        print(j, end=" ")
    print()

for i in range(10):
    for j in range(i+2):
        print(" ",end=" ")
    for j in range(1,9-i):
        print(j, end = " ")
    for j in range(7-i,0,-1):
        print(j, end =" ")
    print()


type(  (2, 3, 4, 5) )
type(  [2, 3, 4, 5] )

x = "This is a sample string"
# x = "0123456789"

print("x=", x)

# Accessing a single character
print("x[0]=", x[0])
print("x[1]=", x[1])

# Accessing from the right side
print("x[-1]=", x[-1])

# Access 0-5
print("x[:6]=", x[:6])
# Access 6
print("x[6:]=", x[6:])
# Access 6-8
print("x[6:9]=", x[6:9])

plain_text = "This is a test. ABC abc"

for c in plain_text:
    print(c, end=" ")

