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

in_str=input("How can I help you?")
pattern=r"[Pp]lease convert (\d+|[a-zA-Z]+)(?: |$)(?:minimally|(?:(?:using )([a-zA-Z]+))$){0,1}"
rst=re.fullmatch(pattern,in_str)
if rst!=None:
    if "using" in in_str:
        ans=""
        if re.match(r"\d+",rst.group(1)):
            ans=NumToOther(rst.group(1),rst.group(2))
        else:
            ans=str(OtherToNum(rst.group(1),rst.group(2)))
        print("Sure! It is "+ans)
    elif "minimally" in in_str:
        pass
    else:
        # N to R
        if re.match(r"\d+",rst.group(1)):
           print(NumToRoman(rst.group(1))) 
        # R to N    
        elif re.match(r"\w+",rst.group(1)):
            Rstr=rst.group(1).upper()
            ans=RomanToNum(Rstr)
            if ans!=None:
                print("Sure! It is "+str(ans))
            else:
                print("Hey, ask me something that's not impossible to do!")
else:
    print("I don't get what you want, sorry mate!")
