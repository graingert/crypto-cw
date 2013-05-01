from H_matrix import paritycheck_matrix

def check_syndrome(codeword, paritycheck):
    syndrome = []
    
    for i in range(len(codeword)):
        syndrome.append(0)
        for p in paritycheck[i]:
            syndrome[i] = (syndrome[i] + (codeword[i] * p))%2
            
    for p in paritycheck:
        syndrome.append(0)
        for i in range(len(codeword)):
            syndrome[len(syndrome)-1] = (syndrome[len(syndrome)-1] + (codeword[i] * p[i]))%2
            
    if 1 in syndrome:
        print "Not a codeword"
    else:
        print "Valid codeword"
    
    
if __name__ == "__main__":
    
    #Transpose H to get H^T
    temp = map(list, paritycheck_matrix())
    rows = []
    for t in temp:
        rows.append(map(int, t))
        
    #Check codewords
    m1 = "101001111000000000000000000000000000000000000000000000000000000"
    m2 = "100001100000000000000000000000000000000000000000000000001000011"
    m3 = "100001100000000000000000000010000000000000000000000000001000011"

    codewords = [map(int, list(m1)), map(int, list(m2)), map(int, list(m3))]

    for c in codewords:
        check_syndrome(c, rows)