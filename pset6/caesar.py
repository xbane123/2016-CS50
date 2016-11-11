import sys

# check CLi argument
if len(sys.argv) != 2 or int(sys.argv[1]) <= 0 :
    print("Usage: python caesar.py k");
    exit(1)
    
# get the argument and asign k to an integer
a1 = sys.argv[1]
k = int(a1)

# get the input text as s
s = input("plaintext: ")

# print the output text after decypher
print("ciphertext: ", end="")
for c in s :
    
    if c.isalpha() and ord(c) > 64 and ord(c) < 91 :
        
        if (ord(c) + k) > 90 :
            print(chr(ord(c) + k - 26), end="")
            
        else :
            print(chr(ord(c) + k), end="")
            
    elif c.isalpha() and ord(c) > 96 and ord(c) < 123 :
        
        if (ord(c) + k) > 122 :
            print(chr(ord(c) + k - 26), end="")
            
        else :
            print(chr(ord(c) + k), end="")
            
    else :
        print(c, end="")
        
print("")
exit(0)
