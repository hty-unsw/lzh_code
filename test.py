import copy
import re

class NoResult(Exception):
    def __init__(self,msg):
        self.msg=msg

Romans={"I":1,"II":2,"III":3,"IV":4,"V":5,"VI":6,"VII":7,"VIII":8,"IX":9,\
        "X":10,"XX":20,"XXX":30,"XL":40,"L":50,"LX":60,"LXX":70,"LXXX":80,"XC":90,\
        "C":100,"CC":200,"CCC":300,"CD":400,"D":500,"DC":600,"DCC":700,"DCCC":800,"CM":900,\
        "M":1000,"MM":2000,"MMM":3000}

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

def is_num(tnum,table):
    token_list=token(tnum)
    #广义罗马数字中为空
    if tnum[0]=='_':
        raise NoResult("no number")
    #广义罗马数字中含有字母表中不存在的字母
    for i in tnum:
        if table.find(i)==-1:
            raise NoResult("no alpha")

    #根据字母表，对广义罗马数字分位
    tmp_table=table[::-1]
    for i in range(len(token_list)):
        #连续出现，但权值为5
        loc=tmp_table.find(token_list[i][0])
        if token_list[i][1]>1 and loc%2==1:
            raise NoResult("number error")
    return False
    

def NumToRoman(num_str):
    if int(num_str)>=4000:
        raise NoResult("to much!")
    if num_str[0]=='0':
        raise NoResult("have a zero head")

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
                    raise NoResult("No right alpha")
            else:
                is_yes=True
        ans+=Romans[rm[0:ptr]]
        rm=rm[ptr:]
    if ans in Romans.values():
        for key,value in Romans.items():
            if value==ans and key!=rm:
                raise NoResult("Number repeat")
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
    #判断字母表中是否有重复项
    if len(table)!=len(set(table)):
        raise NoResult("alpha table error")
    #判断数字是否是0为前导
    if num[0]=='0':
        raise NorResult("zero head")
    #判断字母表是否足够表达数字
    if num[0]=='9' and len(num)*2+1>len(table):
        raise NoResult("too short")
    elif int(num[0])<5 and len(num)*2-1>len(table):
        raise NoResult("too short")
    table=table[::-1]
    ans=""
    for i in range(len(num)):
        if num[i]!='0':
            loc=len(num)-i
            loc=(loc-1)*2
            ans+=ChToNum(int(num[i]),table,loc)
    return ans

def OtherToNum(tnum,table):
    #判断字母表中是否有重复项
    if len(table)!=len(set(table)):
        raise NoResult("alpha table error")
    #判断字符序列是否有不符合组成规则的地方
    if is_num(tnum,table):
        raise NoResult("num error")

    table=table[::-1]
    tnum=tnum[::-1]
    last_loc=-1
    ans=0
    for i in range(len(tnum)):
        loc=table.find(tnum[i])
        if last_loc>loc:
            ans-= (10**(loc//2))*(5 if loc%2==1 else 1)
        else:
            ans+= (10**(loc//2))*(5 if loc%2==1 else 1)
        last_loc=loc
    reverse=NumToOther(str(ans),table[::-1])
    if reverse!=tnum[::-1]:
        raise NoResult("num error")
    return ans


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
    if len(dfs_rst)==0:
        raise NoResult("No right patten")
    for element in dfs_rst:
        dfs_solve({},0,len(element)-1,element,bt_list)
    if len(bt_list)==0:
        raise NoResult("No final result")
    #print("____________________")
    #for element in bt_list:
    #    print(element[0]+":"+str(element[1]))
    minn=0x7f7f7f
    rst_ptr=-1
    for i in range(len(bt_list)):
        if minn>bt_list[i][1]:
            minn=bt_list[i][1]
            rst_ptr=i
    if rst_ptr==-1:
        raise NoResult("No Result")
    else:
        return copy.deepcopy(bt_list[rst_ptr])

#def main():
#    num_list=["MDCCLXXXVII","MDCCLXXXIX","MMMVII","VI","ABCADDEFGF","ABCCDED"]
#    for i in num_list:
#        solve(i)
#

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
                        ans=NumToOther(rst.group(1),rst.group(2))
                    elif re.fullmatch(r"[a-zA-Z_]+",rst.group(1)):
                        ans=str(OtherToNum(rst.group(1),rst.group(2)))
                    else:
                        raise NoResult("error")
                #minimally
                elif "minimally" in in_str:
                    if re.fullmatch(r"[a-zA-Z_]+",rst.group(1)):
                        ans=solve(rst.group(1))
                        ptr=0
                        while ans[0][ptr]=='_':
                            ptr+=1
                        ans[0]=ans[0][ptr:]
                        ans=str(ans[1])+" using "+ans[0]
                    else:
                        raise NoResult("error")
                #others
                else:
                    # N to R
                    if re.fullmatch(r"\d+",rst.group(1)):
                        ans=NumToRoman(rst.group(1))
                    # R to N    
                    elif re.fullmatch(r"[a-zA-Z_]+",rst.group(1)):
                        Rstr=rst.group(1).upper()
                        ans=RomanToNum(Rstr)
                        ans=str(ans)
                    else:
                        raise NoResult("error")
                print("Sure! It is "+ans)
            except NoResult as n:
                #print(n.msg)
                print("Hey, ask me something that's not impossible to do!")
        else:
            print("I don't get what you want, sorry mate!")

if __name__ == '__main__':
    main()
