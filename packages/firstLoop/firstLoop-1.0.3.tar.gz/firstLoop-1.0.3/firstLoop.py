def print_lol(the_list,level):
    for item in the_list:
        if(isinstance(item,list)):
            print_lol(item,level+1)
        else:
            for num in range(level):
                print("\t",end="")
            print(item)