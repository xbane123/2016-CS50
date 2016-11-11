def main() :

    # input the credit card number of 13~16 digits
    while True :
        credit = input("Please enter a credit card number : ")
        if credit.isdecimal() and int(credit) > 0 :
            break

    # for AMEX card
    if len(credit) == 15 and int(credit[0]) == 3 :
        if valid_15(credit) == True :
            print("AMEX")    
        else :
            print("INVALID")
    
    # for MASTER card
    elif len(credit) == 16 and int(credit[0]) == 5 :
        if valid_16(credit) == True :
            print("MASTERCARD")    
        else :
            print("INVALID")

    # for VISA card - 16 digits
    elif len(credit) == 16 and int(credit[0]) == 4 :
        if valid_16(credit) == True :
            print("VISA")    
        else :
            print("INVALID")

    # for VISA card - 13 digits
    elif len(credit) == 13 and int(credit[0]) == 4 :
        if valid_13(credit) == True :
            print("VISA")    
        else :
            print("INVALID")

    # not one of the above conditions
    else :
        print("INVALID")
    
    exit(0)

# len(credit) == 16
def valid_16(credit) :

    sum_even_1 = 0
    sum_even_2 = 0
    for i in range(8) :
        
        if int(credit[2*i]) * 2 >= 10 :
            res = int(credit[2*i]) * 2 % 10
            sum_even_1 += res + (int(credit[2*i]) * 2 - res) / 10
        else :
            sum_even_1 += int(credit[2*i]) * 2

    for i in range(8) :        
        sum_even_2 += int(credit[2*i+1])
           
    #print("{}".format(sum_even_1 + sum_even_2))

    if (sum_even_1 + sum_even_2) % 10 == 0 :
        return True
            
    else :
        return False

# len(credit) == 15
def valid_15(credit) :

    sum_even_1 = 0
    sum_even_2 = 0
    for i in range(7) :
        if int(credit[2*i+1]) * 2 >= 10 :
            res = int(credit[2*i+1]) * 2 % 10
            sum_even_1 += res + (int(credit[2*i+1]) * 2 - res) / 10
        else :
            sum_even_1 += int(credit[2*i+1]) * 2

    for i in range(8) :        
        sum_even_2 += int(credit[2*i])
           
    #print("{}".format(sum_even_1 + sum_even_2))

    if (sum_even_1 + sum_even_2) % 10 == 0 :
        return True
        
    else :
        return False

#len(credit) == 13
def valid_13(credit) :

    sum_even_1 = 0
    sum_even_2 = 0
    for i in range(6) :
        if int(credit[2*i+1]) * 2 >= 10 :
            res = int(credit[2*i+1]) * 2 % 10
            sum_even_1 += res + (int(credit[2*i+1]) * 2 - res) / 10
        else :
            sum_even_1 += int(credit[2*i+1]) * 2

    for i in range(7) :        
        sum_even_2 += int(credit[2*i])
           
    #print("{}".format(sum_even_1 + sum_even_2))

    if (sum_even_1 + sum_even_2) % 10 == 0 :
        return True
            
    else :
        return False

if __name__ == "__main__" :
    main()
