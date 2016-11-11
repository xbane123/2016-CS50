def main():
    while True:
        counter = input("Please enter a number between 0 and 23 : ")
        count = int(counter)
        if count >= 0 and count < 24 :
            break

    if count == 0 :
        exit(1)
    
    for i in range(count):
        spaces(count-1-i)
        hashs(i+1)
        spaces(2)
        hashs(i+1)
        print("")
    exit(0)

def spaces(n):
    for i in range(n):
        print(chr(32), end="")
    
def hashs(n):
    for i in range(n):
        print(chr(35), end="")
    
if __name__ == "__main__":
    main()
