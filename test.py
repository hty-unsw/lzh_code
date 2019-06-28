import copy
import re

Romans={"I":1,"II":2,"III":3,"IV":4,"V":5,"VI":6,"VII":7,"VIII":8,"IX":9,\
        "X":10,"XX":20,"XXX":30,"XL":40,"L":50,"LX":60,"LXX":70,"LXXX":80,"XC":90,\
        "C":100,"CC":200,"CCC":300,"CD":400,"D":500,"DC":600,"DCC":700,"DCCC":800,"CM":900,\
        "M":1000,"MM":2000,"MMM":3000}

def NumToRoman(num_str):
    ans=""
    value=list(Romans.values())
    keys =list(Romans.keys())
    for i in range(len(num_str)):
        if num_str[i]!='0':
            ans+=keys[int(num_str[i])-1+(len(num_str)-i-1)*9]
    return ans

def RomanToNum(rm):
    ans=0
    ptr=0
    while rm!="":
        is_yes=False
        for i in range(len(rm)):
            if rm[0:i+1] not in Romans:
                if is_yes:
                    ptr=i
                    is_yes=False
                    break
                else:
                    return None
            else:
                is_yes=True
        ans+=Romans[rm[0:ptr]]
        rm=rm[ptr:]
    
    if ans in Romans.values():
        for key,value in Romans.items():
            if value==ans and key!=rm:
                return None
    return ans

def ChToNum(num,table,loc):
    ans=""
    if num<=3:
        for i in range(num):
            ans+=table[loc]
    elif num==4:
        ans+=(table[loc]+table[loc+1])
    elif num==5:
        ans+=table[loc+1]
    elif num==6:
        ans+=(table[loc+1]+table[loc])
    elif num==9:
        ans+=(table[loc]+table[loc+2])
    else:
        ans+=table[loc+1]
        for i in range(num-5):
            ans+=table[loc]
    return ans

def NumToOther(num,table):
    table=table[::-1]
    ans=""
    for i in range(len(num)):
        if num[i]!='0':
            loc=len(num)-i
            if len(table)<loc*2:
                return None
            if num[i]=='9' and len(table)<loc*2+1:
                return None
            loc=(loc-1)*2
            ans+=ChToNum(int(num[i]),table,loc)
    return ans

def OtherToNum(tnum,table):
    table=table[::-1]
    tnum=tnum[::-1]
    last_loc=-1
    ans=0
    for i in range(len(tnum)):
        loc=table.find(tnum[i])
        if loc==-1:
            return None
        elif last_loc>loc:
            ans-= (10**(loc//2))*(5 if loc%2==1 else 1)
        else:
            ans+= (10**(loc//2))*(5 if loc%2==1 else 1)
        last_loc=loc
    return ans

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

def dfs(ans,depth,token_list,rst):
    if depth>=len(token_list):
        if test_num(ans):
            tmp=""
            for w in ans:
                for i in w:
                    for k in range(i[1]):
                        tmp+=i[0]
                tmp+=' '
            rst.append(copy.deepcopy(ans))
        return
    for i in range(1,3):
        if i==1:
            ans.append([token_list[depth]])
            dfs(ans,depth+1,token_list,rst)
            ans.pop()
        elif i==2:
            if depth+1<len(token_list):
                ans.append([token_list[depth],token_list[depth+1]])
                dfs(ans,depth+2,token_list,rst)
                ans.pop()
    return


def test_num(dfs_rst):
    for w in dfs_rst:
        if len(w)==2:
            if w[0][1]>1:
                return False
    return True


def dfs_solve(ans,num,depth,dfs_list,bt_list):
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
        bt_list.append([copy.deepcopy(table),copy.deepcopy(num)])
        return
    wei=dfs_list[depth]
    wei_w=10**(len(dfs_list)-depth-1)
    if len(wei)==1:
        if ans.get(wei[0][0])!=None:
            if ans[wei[0][0]]<wei_w:
                return
            if wei[0][1]==1:
                for tmp in [1,5]:
                    num+=tmp*wei_w
                    dfs_solve(ans,num,depth-1,dfs_list,bt_list)
                    num-=tmp*wei_w
            else:
                num+=1*wei_w*wei[0][1]
                dfs_solve(ans,num,depth-1,dfs_list,bt_list)
                num-=1*wei_w*wei[0][1]
        else:
            if wei[0][1]==1:
                for tmp in [1,5]:
                    ans[wei[0][0]]=tmp*wei_w
                    num+=tmp*wei_w
                    dfs_solve(ans,num,depth-1,dfs_list,bt_list)
                    del ans[wei[0][0]]
                    num-=tmp*wei_w
            else:
                ans[wei[0][0]]=1*wei_w
                num+=1*wei_w*wei[0][1]
                dfs_solve(ans,num,depth-1,dfs_list,bt_list)
                del ans[wei[0][0]]
                num-=1*wei_w*wei[0][1]
    else:
        if ans.get(wei[0][0])!=None and ans.get(wei[1][0])==None:
            if ans[wei[0][0]]<wei_w:
                return
            if wei[0][1]==1 and wei[1][1]==1:
                if ans[wei[0][0]]==1*wei_w:
                    #4
                    ans[wei[1][0]]=5*wei_w
                    num+=(5*wei_w-1*wei_w)
                    dfs_solve(ans,num,depth-1,dfs_list,bt_list)
                    num-=(5*wei_w-1*wei_w)
                    del ans[wei[1][0]]
                elif ans[wei[0][0]]==5*wei_w:
                    #6
                    ans[wei[1][0]]=1*wei_w
                    num+=(5*wei_w+1*wei_w)
                    dfs_solve(ans,num,depth-1,dfs_list,bt_list)
                    num-=(5*wei_w+1*wei_w)
                    del ans[wei[1][0]]

                    #9
                    ans[wei[1][0]]=10*wei_w
                    num+=(10*wei_w-1*wei_w)
                    dfs_solve(ans,num,depth-1,dfs_list,bt_list)
                    num-=(10*wei_w-1*wei_w)
                    del ans[wei[1][0]]

            elif wei[0][1]==1 and wei[1][1]>1:
                if ans[wei[0][0]]==1*wei_w:
                    return
                ans[wei[1][0]]=5*wei_w
                num+=(5*wei_w+1*wei_w*wei[1][1])
                dfs_solve(ans,num,depth-1,dfs_list,bt_list)
                num-=(5*wei_w+1*wei_w*wei[1][1])
                del ans[wei[1][0]]
            
        elif ans.get(wei[0][0])==None and ans.get(wei[1][0])!=None:
            if ans[wei[1][0]]<wei_w:
                return
            if wei[0][1]==1 and wei[1][1]==1:
                if ans[wei[1][0]]==1*wei_w:
                    #6
                    ans[wei[0][0]]=5*wei_w
                    num+=(5*wei_w+1*wei_w)
                    dfs_solve(ans,num,depth-1,dfs_list,bt_list)
                    num-=(5*wei_w+1*wei_w)
                    del ans[wei[0][0]]
                elif ans[wei[1][0]]==5*wei_w:
                    #4
                    ans[wei[0][0]]=1*wei_w
                    num+=(5*wei_w-1*wei_w)
                    dfs_solve(ans,num,depth-1,dfs_list,bt_list)
                    num-=(5*wei_w-1*wei_w)
                    del ans[wei[0][0]]

            elif wei[0][1]==1 and wei[1][1]>1:
                if ans[wei[1][0]]==5*wei_w:
                    return
                ans[wei[0][0]]=5*wei_w
                num+=(5*wei_w+1*wei_w*wei[1][1])
                dfs_solve(ans,num,depth-1,dfs_list,bt_list)
                num-=(5*wei_w+1*wei_w*wei[1][1])
                del ans[wei[0][0]]

        elif ans.get(wei[0][0])!=None and ans.get(wei[1][0])!=None:
            if ans[wei[0][0]]<wei_w or ans[wei[1][0]]<wei_w:
                return
            if ans[wei[0][0]]==5*wei_w and ans[wei[1][0]]==5*wei_w:
                return
            if wei[0][1]==1 and wei[1][1]==1:
                if ans[wei[0][0]]==5*wei_w and ans[wei[1][0]]==1*wei_w:
                    #6
                    num+=(5*wei_w+1*wei_w)
                    dfs_solve(ans,num,depth-1,dfs_list,bt_list)
                    num-=(5*wei_w+1*wei_w)

                elif ans[wei[0][0]]==1*wei_w and ans[wei[1][0]]==5*wei_w:
                    #4
                    num+=(5*wei_w-1*wei_w)
                    dfs_solve(ans,num,depth-1,dfs_list,bt_list)
                    num-=(5*wei_w-1*wei_w)

            elif wei[0][1]==1 and wei[1][1]>1:
                if ans[wei[1][0]]!=1*wei_w:
                    return;
                num+=(5*wei_w+1*wei_w*wei[1][1])
                dfs_solve(ans,num,depth-1,dfs_list,bt_list)
                num-=(5*wei_w+1*wei_w*wei[1][1])

        elif ans.get(wei[0][0])==None and ans.get(wei[1][0])==None:
            if wei[0][1]==1 and wei[1][1]==1:
                #6
                ans[wei[0][0]]=5*wei_w
                ans[wei[1][0]]=1*wei_w
                num+=(5*wei_w+1*wei_w)
                dfs_solve(ans,num,depth-1,dfs_list,bt_list)
                del ans[wei[0][0]]
                del ans[wei[1][0]]
                num-=(5*wei_w+1*wei_w)

                #4
                ans[wei[0][0]]=1*wei_w
                ans[wei[1][0]]=5*wei_w
                num+=(5*wei_w-1*wei_w)
                dfs_solve(ans,num,depth-1,dfs_list,bt_list)
                del ans[wei[0][0]]
                del ans[wei[1][0]]
                num-=(5*wei_w-1*wei_w)

                #9
                ans[wei[0][0]]=1*wei_w
                ans[wei[1][0]]=10*wei_w
                num+=(10*wei_w-1*wei_w)
                dfs_solve(ans,num,depth-1,dfs_list,bt_list)
                del ans[wei[0][0]]
                del ans[wei[1][0]]
                num-=(10*wei_w-1*wei_w)

            elif wei[0][1]==1 and wei[1][1]>1:
                ans[wei[0][0]]=5*wei_w
                ans[wei[1][0]]=1*wei_w
                num+=(5*wei_w+1*wei_w*wei[1][1])
                dfs_solve(ans,num,depth-1,dfs_list,bt_list)
                del ans[wei[0][0]]
                del ans[wei[1][0]]
                num-=(5*wei_w+1*wei_w*wei[1][1])
    return
            

def solve(num): 
    token_list=token(num)
    dfs_rst=[]
    bt_list=[]
    dfs([],0,token_list,dfs_rst)
    for element in dfs_rst:
        dfs_solve({},0,len(element)-1,element,bt_list)
    print("____________________")
    for element in bt_list:
        print(element[0]+":"+str(element[1]))
    minn=0x7f7f7f
    rst_ptr=-1
    for i in range(len(bt_list)):
        if minn>bt_list[i][1]:
            minn=bt_list[i][1]
            rst_ptr=i
    print(bt_list[rst_ptr][0],bt_list[rst_ptr][1])

def main():
    num_list=["MDCCLXXXVII","MDCCLXXXIX","MMMVII","VI","ABCADDEFGF","ABCCDED"]
    for i in num_list:
        solve(i)

if __name__ == '__main__':
    main()


#in_str=input("How can I help you?")
#pattern=r"[Pp]lease convert (\d+|[a-zA-Z]+)(?: |$)(?:minimally|(?:(?:using )([a-zA-Z]+))$){0,1}"
#rst=re.fullmatch(pattern,in_str)
#if rst!=None:
#    if "using" in in_str:
#        ans=""
#        if re.match(r"\d+",rst.group(1)):
#            ans=NumToOther(rst.group(1),rst.group(2))
#        else:
#            ans=str(OtherToNum(rst.group(1),rst.group(2)))
#        print("Sure! It is "+ans)
#    elif "minimally" in in_str:
#        pass
#    else:
#        # N to R
#        if re.match(r"\d+",rst.group(1)):
#           print(NumToRoman(rst.group(1))) 
#        # R to N    
#        elif re.match(r"\w+",rst.group(1)):
#            Rstr=rst.group(1).upper()
#            ans=RomanToNum(Rstr)
#            if ans!=None:
#                print("Sure! It is "+str(ans))
#            else:
#                print("Hey, ask me something that's not impossible to do!")
#else:
#    print("I don't get what you want, sorry mate!")
