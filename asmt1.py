import re
import copy

class error(Exception):
    def __init__(self,msg):
        self.msg=msg

###############################################################################################
#problem one

Romans={"I":1,"II":2,"III":3,"IV":4,"V":5,"VI":6,"VII":7,"VIII":8,"IX":9,\
        "X":10,"XX":20,"XXX":30,"XL":40,"L":50,"LX":60,"LXX":70,"LXXX":80,"XC":90,\
        "C":100,"CC":200,"CCC":300,"CD":400,"D":500,"DC":600,"DCC":700,"DCCC":800,"CM":900,\
        "M":1000,"MM":2000,"MMM":3000}

def NumToRomans(num):
    if not num.isdigit():
        raise error("number not isdigit")
    if len(num)>0 and num[0]=='0':
        raise error("number have 0 first")
    if int(num)>3999:
        raise error("number too big")
    ans=""
    value=list(Romans.values())
    key=list(Romans.keys())
    for i in range(len(num)):
        if num[i]!='0':
            ans+=key[int(num[i])-1 + (len(num)-i-1)*9]
    return ans

def RomansToNum(romans):
    origin_romans=romans
    ans=0
    ptr=0
    while len(romans)>0:
        flag=False
        for i in range(1,len(romans)+1):
            if romans[0:i] in Romans:
                flag=True
                ptr=i
            else:
                if flag:
                    flag=False
                    break
                else:
                    raise error("romans format error")
        ans+=Romans[romans[:ptr]]
        if len(romans)-ptr>0:
            romans=romans[ptr:]
        else:
            break
    if ans in Romans.values():
        for k,v in Romans.items():
            if v==ans and k!=romans:
                raise error("number repeat")

    if NumToRomans(str(ans))!=origin_romans:
        raise error("something wrong")
    return ans

#debug-NumToRomans():
#print(NumToRomans("123"))
#print(NumToRomans("023"))
#print(NumToRomans("adsf"))
#print(NumToRomans("3000"))
#print(NumToRomans("8000"))

#debug-RomansToNum():
#print(RomansToNum("IIII"))
#print(RomansToNum("IXI"))
#print(RomansToNum("MCMLXXXII"))
#print(RomansToNum("MMMVII"))
#print(RomansToNum("ABC"))
#print(RomansToNum("I"))
#print(RomansToNum("III"))

###############################################################################################
#problem two


def NumToGRomans(num,table):
    if len(table)!=len(set(table)):
        raise error("talbe alpha repeat")
    if not num.isdigit():
        raise error("number not isdigit")
    if len(num)>0 and num[0]=='0':
        raise error("number have 0 first")
    if num[0]=='9' and len(num)*2+1>len(table):
        raise error("table too short:=9")
    elif int(num[0])<5 and len(num)*2-1>len(table):
        raise error("table too short:<5")
    elif int(num[0])>=5 and len(num)*2>len(table):
        raise error("table too short:>5")
    reverse_table=table[::-1]
    ans=""
    for i in range(len(num)):
        if num[i]!='0':
            loc=((len(num)-i)-1)*2
            tmp_ans=""
            tmp_num=int(num[i])
            if tmp_num<=3:
                for i in range(tmp_num):
                    tmp_ans+=reverse_table[loc]
            elif tmp_num==4:
                tmp_ans+=(reverse_table[loc]+reverse_table[loc+1])
            elif tmp_num==5:
                tmp_ans+=reverse_table[loc+1]
            elif tmp_num==6:
                tmp_ans+=(reverse_table[loc+1]+reverse_table[loc])
            elif tmp_num==9:
                tmp_ans+=(reverse_table[loc]+reverse_table[loc+2])
            else:
                tmp_ans+=reverse_table[loc+1]
                for i in range(tmp_num-5):
                    tmp_ans+=reverse_table[loc]
            ans+=tmp_ans
    return ans


def GRomansToNum(gromans,table):
    if len(table)!=len(set(table)):
        raise error("talbe alpha repeat")
    if gromans=="_":
        raise error("gromans empty")
    for i in gromans:
        if table.find(i)==-1:
            raise error("no alpha")
    reverse_table=table[::-1]
    reverse_gromans=gromans[::-1]
    ans=0
    last_loc=-1
    for i in range(len(reverse_gromans)):
        loc=reverse_table.find(reverse_gromans[i])
        if last_loc>loc:
            ans-= (10**(loc//2))*(5 if loc%2==1 else 1)
        else:
            ans+= (10**(loc//2))*(5 if loc%2==1 else 1)
        last_loc=loc
    if NumToGRomans(str(ans),table)!=gromans:
        raise error("gromans error")
    return ans

    

#debug-NumToGRomans():
#print(NumToGRomans("123","ABC"))    
#print(NumToGRomans("49036","fFeEdDcCbBaA"))    
#print(NumToGRomans("899999999999","AaBbCcDdEeFfGgHhIiJjKkLl"))    
#print(NumToGRomans("1900604","LAQMPVXYZIRSGN"))    

#debug-GRomansToNum():
#print(GRomansToNum("XXXVI","VI"))
#print(GRomansToNum("XXXVI","IVX"))
#print(GRomansToNum("XXXVI","XWVI"))
#print(GRomansToNum("I","II"))
#print(GRomansToNum("_","_"))
#print(GRomansToNum("XXXVI","XVI"))
#print(GRomansToNum("XXXVI","XABVI"))
#print(GRomansToNum("EeDEBBBaA","fFeEdDcCbBaA"))
#print(GRomansToNum("ABCDEFGHIJKLMNOPQRST","AbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStT"))


###############################################################################################
#problem three

def token(num_a):
    cnt=1
    rst=[[num_a[0],1]]
    rst_ptr=0
    for i in range(1,len(num_a)):
        if num_a[i]==rst[rst_ptr][0]:
            rst[rst_ptr][1]+=1
        else:
            rst.append([num_a[i],1])
            rst_ptr+=1
    return rst

def test_num(dfs_rst):
    for w in dfs_rst:
        if len(w)==2:
            if w[0][1]>1:
                return False
    return True


def dfs_partition(ans,depth,token_list,rst):
    if depth>=len(token_list):
        if test_num(ans):
            #tmp=""
            #for w in ans:
            #    for i in w:
            #        for k in range(i[1]):
            #            tmp+=i[0]
            #    tmp+=' '
            #print(tmp)
            rst.append(copy.deepcopy(ans))
        return
    ans.append([token_list[depth]])
    dfs_partition(ans,depth+1,token_list,rst)
    ans.pop()
    if depth+1<len(token_list):
        ans.append([token_list[depth],token_list[depth+1]])
        dfs_partition(ans,depth+2,token_list,rst)
        ans.pop()
    return

def dfs_assignment(ans,num,depth,dfs_list,bt_list):
    if depth==-1:
        table=""
        new_ans={v:k for k,v in ans.items()}
        for i in range(len(dfs_list)):
            if new_ans.get(1*(10**i))!=None:
                table=new_ans[1*(10**i)]+table
            else:
                table='_'+table
            if new_ans.get(5*(10**i))!=None:
                table=new_ans[5*(10**i)]+table
            else:
                table='_'+table
        ptr=0
        while table[ptr]=='_':
            ptr+=1
        table=table[ptr:]
        bt_list.append([copy.deepcopy(table),copy.deepcopy(num)])
        return
    w=dfs_list[depth]
    w_w=10**(len(dfs_list)-depth-1)
    if len(w)==1:
        if ans.get(w[0][0])!=None:
            if ans[w[0][0]]<w_w:
                return
            #1 5
            if w[0][1]==1:
                for tmp in [1,5]:
                    num+=tmp*w_w
                    dfs_assignment(ans,num,depth-1,dfs_list,bt_list)
                    num-=tmp*w_w
            else:
            #2 3
                num+=1*w_w*w[0][1]
                dfs_assignment(ans,num,depth-1,dfs_list,bt_list)
                num-=1*w_w*w[0][1]
        else:
            #1 5
            if w[0][1]==1:
                for tmp in [1,5]:
                    ans[w[0][0]]=tmp*w_w
                    num+=tmp*w_w
                    dfs_assignment(ans,num,depth-1,dfs_list,bt_list)
                    del ans[w[0][0]]
                    num-=tmp*w_w
            #2 3
            else:
                ans[w[0][0]]=1*w_w
                num+=1*w_w*w[0][1]
                dfs_assignment(ans,num,depth-1,dfs_list,bt_list)
                del ans[w[0][0]]
                num-=1*w_w*w[0][1]
    else:
        if ans.get(w[0][0])!=None and ans.get(w[1][0])==None:
            if ans[w[0][0]]<w_w:
                return
            if w[0][1]==1 and w[1][1]==1:
                if ans[w[0][0]]==1*w_w:
                    #4
                    ans[w[1][0]]=5*w_w
                    num+=(5*w_w-1*w_w)
                    dfs_assignment(ans,num,depth-1,dfs_list,bt_list)
                    num-=(5*w_w-1*w_w)
                    del ans[w[1][0]]

                    #9
                    ans[w[1][0]]=10*w_w
                    num+=(10*w_w-1*w_w)
                    dfs_assignment(ans,num,depth-1,dfs_list,bt_list)
                    num-=(10*w_w-1*w_w)
                    del ans[w[1][0]]

                elif ans[w[0][0]]==5*w_w:
                    #6
                    ans[w[1][0]]=1*w_w
                    num+=(5*w_w+1*w_w)
                    dfs_assignment(ans,num,depth-1,dfs_list,bt_list)
                    num-=(5*w_w+1*w_w)
                    del ans[w[1][0]]

            elif w[0][1]==1 and w[1][1]>1:
                if ans[w[0][0]]==1*w_w:
                    return
                #7 8
                ans[w[1][0]]=5*w_w
                num+=(5*w_w+1*w_w*w[1][1])
                dfs_assignment(ans,num,depth-1,dfs_list,bt_list)
                num-=(5*w_w+1*w_w*w[1][1])
                del ans[w[1][0]]
            
        elif ans.get(w[0][0])==None and ans.get(w[1][0])!=None:
            if ans[w[1][0]]<w_w:
                return
            if w[0][1]==1 and w[1][1]==1:
                if ans[w[1][0]]==1*w_w:
                    #6
                    ans[w[0][0]]=5*w_w
                    num+=(5*w_w+1*w_w)
                    dfs_assignment(ans,num,depth-1,dfs_list,bt_list)
                    num-=(5*w_w+1*w_w)
                    del ans[w[0][0]]
                elif ans[w[1][0]]==5*w_w:
                    #4
                    ans[w[0][0]]=1*w_w
                    num+=(5*w_w-1*w_w)
                    dfs_assignment(ans,num,depth-1,dfs_list,bt_list)
                    num-=(5*w_w-1*w_w)
                    del ans[w[0][0]]
            #7 8
            elif w[0][1]==1 and w[1][1]>1:
                if ans[w[1][0]]==5*w_w:
                    return
                ans[w[0][0]]=5*w_w
                num+=(5*w_w+1*w_w*w[1][1])
                dfs_assignment(ans,num,depth-1,dfs_list,bt_list)
                num-=(5*w_w+1*w_w*w[1][1])
                del ans[w[0][0]]

        elif ans.get(w[0][0])!=None and ans.get(w[1][0])!=None:
            if ans[w[0][0]]<w_w or ans[w[1][0]]<w_w:
                return
            if ans[w[0][0]]==5*w_w and ans[w[1][0]]==5*w_w:
                return
            if w[0][1]==1 and w[1][1]==1:
                if ans[w[0][0]]==5*w_w and ans[w[1][0]]==1*w_w:
                    #6
                    num+=(5*w_w+1*w_w)
                    dfs_assignment(ans,num,depth-1,dfs_list,bt_list)
                    num-=(5*w_w+1*w_w)

                elif ans[w[0][0]]==1*w_w and ans[w[1][0]]==5*w_w:
                    #4
                    num+=(5*w_w-1*w_w)
                    dfs_assignment(ans,num,depth-1,dfs_list,bt_list)
                    num-=(5*w_w-1*w_w)

            #7 8
            elif w[0][1]==1 and w[1][1]>1:
                if ans[w[1][0]]!=1*w_w:
                    return;
                num+=(5*w_w+1*w_w*w[1][1])
                dfs_assignment(ans,num,depth-1,dfs_list,bt_list)
                num-=(5*w_w+1*w_w*w[1][1])

        elif ans.get(w[0][0])==None and ans.get(w[1][0])==None:
            if w[0][1]==1 and w[1][1]==1:
                #6
                ans[w[0][0]]=5*w_w
                ans[w[1][0]]=1*w_w
                num+=(5*w_w+1*w_w)
                dfs_assignment(ans,num,depth-1,dfs_list,bt_list)
                del ans[w[0][0]]
                del ans[w[1][0]]
                num-=(5*w_w+1*w_w)

                #4
                ans[w[0][0]]=1*w_w
                ans[w[1][0]]=5*w_w
                num+=(5*w_w-1*w_w)
                dfs_assignment(ans,num,depth-1,dfs_list,bt_list)
                del ans[w[0][0]]
                del ans[w[1][0]]
                num-=(5*w_w-1*w_w)

                #9
                ans[w[0][0]]=1*w_w
                ans[w[1][0]]=10*w_w
                num+=(10*w_w-1*w_w)
                dfs_assignment(ans,num,depth-1,dfs_list,bt_list)
                del ans[w[0][0]]
                del ans[w[1][0]]
                num-=(10*w_w-1*w_w)

            elif w[0][1]==1 and w[1][1]>1:
                ans[w[0][0]]=5*w_w
                ans[w[1][0]]=1*w_w
                num+=(5*w_w+1*w_w*w[1][1])
                dfs_assignment(ans,num,depth-1,dfs_list,bt_list)
                del ans[w[0][0]]
                del ans[w[1][0]]
                num-=(5*w_w+1*w_w*w[1][1])
    return

def solve(num): 
    token_list=token(num)
    partition_patterns_list=[]
    assignment_patterns_list=[]

    dfs_partition([],0,token_list,partition_patterns_list)
    if len(partition_patterns_list)==0:
        raise error("No right patten")
    for element in partition_patterns_list:
        dfs_assignment({},0,len(element)-1,element,assignment_patterns_list)
    if len(assignment_patterns_list)==0:
        raise error("No final result")
    minn=0x7f7f7f
    rst_ptr=-1
    for i in range(len(assignment_patterns_list)):
        if minn>assignment_patterns_list[i][1]:
            minn=assignment_patterns_list[i][1]
            rst_ptr=i
    if rst_ptr==-1:
        raise error("No Result")
    else:
        return copy.deepcopy(assignment_patterns_list[rst_ptr])

#debug-solve()
#print(solve("ABCD"))
#print(solve("OI"))
#print(solve("ABAA"))
#print(solve("ABCDEFA"))
#print(solve("MDCCLXXXVII"))
#print(solve("MDCCLXXXIX"))
#print(solve("MMMVII"))
#print(solve("VI"))
#print(solve("ABCADDEFGF"))
#print(solve("ABCCDED"))
#print(solve("I"))
#print(solve("XI"))

###############################################################################################
#main
import fileinput

def main():
    f_in=fileinput.input()
    for in_str in f_in:
        in_str=in_str[:-1]
        #in_str=input("How can I help you?")
        pattern=r"Please convert ([_0-9a-zA-Z]+)(?: |$)(?:minimally|(?:(?:using )([a-zA-Z]+|_))$){0,1}"
        rst=re.fullmatch(pattern,in_str)
        if rst!=None:
            ans=""
            try:
                #Using 
                if "using" in in_str:
                    if re.fullmatch(r"\d+",rst.group(1)):
                        ans=NumToGRomans(rst.group(1),rst.group(2))
                    elif re.fullmatch(r"[a-zA-Z_]+",rst.group(1)):
                        ans=str(GRomansToNum(rst.group(1),rst.group(2)))
                    else:
                        raise error("error")
                #minimally
                elif "minimally" in in_str:
                    if re.fullmatch(r"[a-zA-Z_]+",rst.group(1)):
                        ans=solve(rst.group(1))
                        ans=str(ans[1])+" using "+ans[0]
                    else:
                        raise error("error")
                #others
                else:
                    # N to R
                    if re.fullmatch(r"\d+",rst.group(1)):
                        ans=NumToRomans(rst.group(1))
                    # R to N    
                    elif re.fullmatch(r"[a-zA-Z_]+",rst.group(1)):
                        Rstr=rst.group(1).upper()
                        ans=RomansToNum(Rstr)
                        ans=str(ans)
                    else:
                        raise error("error")
                print("Sure! It is "+ans)
            except error as n:
                #print(n.msg)
                print("Hey, ask me something that's not impossible to do!")
        else:
            print("I don't get what you want, sorry mate!")

if __name__ == '__main__':
    main()
