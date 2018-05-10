def sum( one, two):
    
    one_int = convert_int(one)
    two_int = convert_int(two)
    
    res = one_int + two_int
    
    return res

def convert_int(num):
    
    converted = int(num)
    return converted

answer = sum("1","2")
print(answer)



    
    
    
    
    