def generator_matrix():
    #Specify the identity matrix (n-k), to
    #generate matrix P^T
    ident = ["100000", "010000", "001000", "000100", "000010", "000001"]
    col = []

    #Generate all non-zero binary m-tuples not in
    #the identity matrix
    for x in range(1, 64):
        bin_string = bin(x)[2:].zfill(6)
        
        if not(bin_string in ident):
            col.append(bin_string)
            
    #Transpose P^T to get P
    new_col = []

    for i in range(6):
        new_col.append("")
        
        for c in col:
            new_col[i] = "{0}{1}".format(new_col[i], c[i])

    #Create the identity matrix (k)
    ident = []
    zero = ""
    for x in range(57):
        zero = "{0}{1}".format(zero, "0")

    for x in range(57):
        temp = list(zero)
        temp[x] = "1"
        temp = "".join(temp)
        ident.append(temp)

    ident.extend(new_col)
    return list(ident)
    
if __name__ == "__main__":
    col = generator_matrix()

    #Due to the large size, print to three outputs (in LaTeX
    #typesetting) for legibility
    g1 = open("output/g1.txt", "w")
    g2 = open("output/g2.txt", "w")
    g3 = open("output/g3.txt", "w")
        
    for y in range(57):
        for x in range (21):
            if x < 20:
                g1.write("{0} & ".format(col[x][y]))
            else:
                g1.write("{0}".format(col[x][y]))
                
        g1.write("\\\\\n")
        
        for x in range (21, 42):
            if x < 41:
                g2.write("{0} & ".format(col[x][y]))
            else:
                g2.write("{0}".format(col[x][y]))
                
        g2.write("\\\\\n")
                
        for x in range (42, 63):
            if x < 62:
                g3.write("{0} & ".format(col[x][y]))
            else:
                g3.write("{0}".format(col[x][y]))
                
        g3.write("\\\\\n")