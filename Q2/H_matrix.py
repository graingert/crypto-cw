def paritycheck_matrix():
    #Specify the identity matrix
    ident = ["100000", "010000", "001000", "000100", "000010", "000001"]
    col = []

    #Generate all non-zero binary m-tuples not in
    #the identity matrix
    for x in range(1, 64):
        bin_string = bin(x)[2:].zfill(6)
        
        if not(bin_string in ident):
            col.append(bin_string)
        
    #Append the identity matrix
    for x in ident:
        col.append(x)
        
    return col
    
if __name__ == "__main__":
    col = paritycheck_matrix()

    #Due to the large size, print to three outputs (in LaTeX
    #typesetting) for legibility
    h1 = open("output/h1.txt", "w")
    h2 = open("output/h2.txt", "w")
    h3 = open("output/h3.txt", "w")
        
    for y in range(6):
        for x in range (21):
            if x < 20:
                h1.write("{0} & ".format(col[x][y]))
            else:
                h1.write("{0}".format(col[x][y]))
                
        h1.write("\\\\\n")
        
        for x in range (21, 42):
            if x < 41:
                h2.write("{0} & ".format(col[x][y]))
            else:
                h2.write("{0}".format(col[x][y]))
                
        h2.write("\\\\\n")
                
        for x in range (42, 63):
            if x < 62:
                h3.write("{0} & ".format(col[x][y]))
            else:
                h3.write("{0}".format(col[x][y]))
                
        h3.write("\\\\\n")