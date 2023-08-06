#author: abi
""" this is comment"""
def printname(listt):
    for i in listt:
        if isinstance(i,list):
            printname(i)
        else:
            print(i)
"""this is the end of text"""
