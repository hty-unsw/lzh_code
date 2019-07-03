# Written by Eric Martin for COMP9021
#
# Prompts the user for an arity (a natural number) n and a word.
# Call symbol a word consisting of nothing but alphabetic characters
# and underscores.
# Checks that the word is valid, in that it satisfies the following
# inductive definition:
# - a symbol, with spaces allowed at both ends, is a valid word;
# - a word of the form s(w_1,...,w_n) with s denoting a symbol and
#   w_1, ..., w_n denoting valid words, with spaces allowed at both ends
#   and around parentheses and commas, is a valid word.


import sys
import re
import fileinput

class Error(Exception):
    def __init__(self,msg):
        Error.msg=msg


def token(in_str):
    token_list=list()
    tmp_list=re.findall(r"[_a-zA-Z]+|\(|\)|,| ",in_str)
    #print(tmp_list)
    tmp_len=0
    for token in tmp_list:
        if re.fullmatch(r"[_a-zA-Z]+",token):
            token_list.append([token,0])
            tmp_len+=len(token)
        elif re.fullmatch(r"\(|\)",token):
            token_list.append([token,1])
            tmp_len+=1
        elif token==',':
            token_list.append([token,2])
            tmp_len+=1
        elif token==' ':
            token_list.append([token,3])
            tmp_len+=1
    if tmp_len!=len(in_str):
        raise Error("Length Error")
    return token_list

def is_word_brackets(tl,rg,n,depth):
    if len(tl)<4:
        raise Error("not brackets word")
    while tl[rg[0]][0]==' ':
        rg[0]+=1
    while tl[rg[1]][0]==' ':
        rg[1]-=1
    #tmp=""
    #for i in range(rg[0],rg[1]+1):
    #    tmp+=tl[i][0]
    #tmp="is_brackets_word : "+tmp
    #print(tmp)
    tmp=rg[0]
    try:
        while tl[tmp][0]!='(':
            tmp+=1
        tmp-=1
    except:
        raise Error("out of range")
    if not is_word_symbol(tl,[rg[0],tmp],depth+1):
        raise Error("Format Error - not a symbol")
    rg[0]=tmp+1
    if tl[rg[0]][0]!='(' or tl[rg[1]][0]!=')':
        raise Error("Format Error - brackets")
    rg[0]+=1
    rg[1]-=1
    tmp_cnt=0
    brackets_list=list()
    tmp_stack=list()
    flag=True
    for i in range(rg[0],rg[1]+1):
        if tl[i][0]=='(':
            tmp_stack.append(1)
        elif tl[i][0]==')':
            if len(tmp_stack)>=1:
                tmp_stack.pop()
            else:
                raise Error("Brackets Error")
        elif tl[i][0]==',':
            if len(tmp_stack)==0:
                brackets_list.append(i)
    if len(brackets_list)!=n-1:
        raise Error("Less Error")
    brackets_list.append(rg[1]+1)
    #print(brackets_list)
    for i in range(n):
        try:
            is_word(tl,[rg[0],brackets_list[i]-1],n,depth+1)
            rg[0]=brackets_list[i]+1
        except Exception as error:
            #print(error.msg)
            return False
    return True

def is_word_symbol(tl,rg,depth):
    while tl[rg[0]][0]==' ':
        rg[0]+=1
    while tl[rg[1]][0]==' ':
        rg[1]-=1
    #tmp=""
    #for i in range(rg[0],rg[1]+1):
    #    tmp+=tl[i][0]
    #tmp="is_symbol_word : "+tmp
    #print(tmp)
    if tl[rg[0]][1]==0:
        return True
    return False


def is_word(tl,rg,n,depth):
    while tl[rg[0]][0]==' ':
        rg[0]+=1
    while tl[rg[1]][0]==' ':
        rg[1]-=1
    #tmp=""
    #for i in range(rg[0],rg[1]+1):
    #    tmp+=tl[i][0]
    #tmp="is_word : "+tmp
    #print(tmp)
    if depth==0 and n>1:
        return is_word_brackets(tl,rg,n,depth+1)
    for i in range(rg[0],rg[1]+1):
        if tl[i][1]==1:
            return is_word_brackets(tl,rg,n,depth+1)
    return is_word_symbol(tl,rg,depth+1)


def is_valid(word, arity):
    try:
        token_list=token(word)
        return is_word(token_list,[0,len(token_list)-1],arity,0)
    except Exception as error:
        #print(error.msg)
        return False
    return False
    # REPLACE THE RETURN STATEMENT ABOVE WITH YOUR CODE

try:
    arity = int(input('Input an arity : '))
    if arity < 0:
        raise ValueError
except ValueError:
    print('Incorrect arity, giving up...')
    sys.exit()
word = input('Input a word: ')
if is_valid(word, arity):
    print('The word is valid.')
else:
    print('The word is invalid.')

