#------------------------------------------------------------------#
#                   Traversing a List
#------------------------------------------------------------------#
def traversing_list (the_list,level=0):# define a function for traversing list -->level=0 meaning this parameter is optional.
    for son_list in the_list:
        if isinstance(son_list,list):
            traversing_list(son_list,level+1)#if son_list is also a list we can
        else:
            for tab_stop in range(level):
                print("\t",end='')
            print(son_list)