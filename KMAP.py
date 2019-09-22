# CSE 101
# K-Map Minimization 
# Name: VANSHIKA GOEL
# Section: A
# Date: 12/10/2018

import copy
def convert(n,ans):
    """
    This python function converts binary representation and
    dashed binary representation ( from Quine McCluskey algorithm )
    into terms which will be included in the minimized function.

    Input is the binary and dashed binary representation of the format
    'abab' (where a and b are either 0 or 1 (for n=4; where n is number of variables).
    Output is a string representing a term of Boolean Expression in SOP form
    """
    # n is the no of variables which cannot be greater than 4
    # Assuming n=0 and n>4 as invalid inputs
    n=int(n)
    ans=str(ans)
    st=""
    if n>=1:
        if ans[0]=='1':
            st=st+"w"
        if ans[0]=='0':
            st=st+"w'"
        if ans[0]=="-":
            st=st
        if n>=2:
            if ans[1]=='1':
                st=st+"x"
            if ans[1]=='0':
                st=st+"x'"
            if ans[1]=="-":
                st=st
            if n>=3:
                if ans[2]=='1':
                    st=st+"y"
                if ans[2]=='0':
                    st=st+"y'"
                if ans[2]=="-":
                    st=st
                if n>=4:
                    if ans[3]=='1':
                        st=st+"z"
                    if ans[3]=='0':
                        st=st+"z'"
                    if ans[3]=="-":
                        st=st
    return st      
    
def EPI(row,col=[]):
    """
    This python Function takes two list as input. First list(row)
    consist of minterms whose value is 1. Second list(col) consist of
    possible combinations that can be essential prime implicant
    Output is a list containing essential prime impicants

    First Input list is of the format [c0,c1,c2,...,cn] and second list
    if of the format [[p0,p1,..pj],[t0,t1,..tm],...[k0,k1,...kt]]
    Output is a list of EPI.
    """
    rowlen=len(row)
    collen=len(col)
    rtable=[0]*(rowlen+1)
    # fco is iterating over rows in first column
    # ie is iterating over col list
    fco=1
    ie=0
    cta=[0]*(collen+1)
    while ie<collen:
        cta[fco]=col[ie]
        rtable[0]=cta
        fco=fco+1
        ie=ie+1
    # fr is iterating over columns
    # ch is iterating over elements of row list
    fr=1
    ch=0
    while fr<rowlen+1:
        ctable=[0]*(collen+1)
        ctable[0]=row[ch]
        rtable[fr]=ctable
        ch=ch+1
        fr=fr+1
    # Making a list(rtable) for implementing Petrick's method
    a=1
    while a<collen+1:
        i=0
        term=rtable[0][a]
        while i<len(term):
            j=1
            while j<rowlen+1:
                if term[i]==rtable[j][0]:
                    rtable[j][a]='X'
                    j=j+1
                else:
                    j=j+1
            i=i+1
        a=a+1
 # t keeps the track for iterating over rows       
 # c is iterating over columns
 # Implementing Petrick method 
    t=1
    FINAL_ANS=[]
    while t<rowlen+1:
        c=1
        count=0
        while c<collen+1:
            if rtable[t][c]=='X':
                count=count+1
                req=c
                c=c+1
            else:
                c=c+1
        if count==1:
            # Finding columns which contain only a single 'X'
            FINAL_ANS.append(rtable[0][req])
            r=1
            while r<collen+1:
                rtable[t][r]='-'
                r=r+1
            k=1
            while k<rowlen+1:
                if rtable[k][req]!='X':
                    rtable[k][req]='-'
                    k=k+1
                else:
                    tr=k
                    l=1
                    while l<collen+1:
                        rtable[tr][l]='-'
                        l=l+1
                    k=k+1
        t=t+1
    # X is the count of 'X' left in the list
    lr=1
    X=0
    while lr<collen+1:
        lc=1
        while lc<rowlen+1:
            if rtable[lc][lr]=='X':
                X=X+1
                lc=lc+1
            else:
                lc=lc+1
        lr=lr+1
    while X != 0:
        # Finding row which contains maximum number of 'X' and appending the row header(prime implicant) in the final answer
        maxval=0
        ir=1
        while ir<collen+1:
            ic=1
            cnt=0
            while ic<rowlen+1:
                if rtable[ic][ir]=='X':
                    cnt=cnt+1
                    ic=ic+1
                else:
                    ic=ic+1
            if cnt>maxval:
                maxval=cnt
                rowno=ir
            ir=ir+1    
        if maxval != 0:
            FINAL_ANS.append(rtable[0][rowno])
            re=1
            while re<rowlen+1:
                if rtable[re][rowno]=='X':
                    rt=1
                    while rt<collen+1:
                        rtable[re][rt]='-'
                        rt=rt+1
                    re=re+1
                else:
                    rtable[re][rowno]='-'
                    re=re+1       
        lr1=1
        X=0
        while lr1<collen+1:
            lc1=1
            while lc1<rowlen+1:
                if rtable[lc1][lr1]=='X':
                    X=X+1
                    lc1=lc1+1
                else:
                    lc1=lc1+1
            lr1=lr1+1    
    return FINAL_ANS


def pi(il=[],sl=[],rest=[],prime=[]):
    """
    This python function makes sure that all the terms in the initial minterm
    list are covered under atleast one prime implicant.

    Input are strings; one of which includes minterms to be checked, while other
    contains groups containing combined terms.
    Output are list; one of which include terms which are not found in any group(This list can be empty)
    other have final combined list
    """
    if len(il)!=0 and len(sl)!=0:
        v=0
        while v<len(sl):
            w=0
            while w<len(sl[v]):
                u=0
                t=0
                while u<len(il):
                    if il[t]==sl[v][w]:
                        if sl[v] not in prime:
                            prime.append(sl[v])
                        t=u    
                        il.pop(u)    
                    else:
                        t=t+1
                        u=u+1
                w=w+1
            v=v+1
        return il,prime
    else:
        return il,prime

def check(n,f=[],s=[],a=[],b=[]):
    """
    This python function checks whether any minterms can be combined according
    to Quine McCluskey Algorithm and finds out the dashed binary representation for
    the same combination.

    Input are lists which contain minterms which need to be checked and combined(if possible)
    and their corresponding binary representation in separate lists.
    Outputs are lists with terms combined and their dashed binary representation
    """
    n=int(n)
    group=[]
    combine=[]
    m=0
    c=0
    t=0
    while m<len(f) and f[m] != 0:
        g=0
        while g<len(s) and s[g] != 0:
            e1=f[m]
            e2=s[g]
            e3=a[m]
            e4=b[g]
            type(e4)
            e1=str(e1)
            e2=str(e2)
            e=0
            count=0
            while e<n:
                if e1[e]==e2[e]:
                    count=count+1
                    e=e+1
                else:
                    dash=e
                    e=e+1
            if count == n-1:
                put=e1[0:dash]+'-'+e1[dash+1:]
                if put not in group:
                    group.append(put)
                combine.append([e3,e4])    
                c=c+1
                t=t+1    
            g=g+1
        m=m+1
    return group,combine

def check1(n,f=[],s=[],a=[],b=[]):
    """
    This Python function takes lists as inputs whose elements are to be checked
    for combining according to QuineMcCluskey Algorithm.

    Input are two lists of the format [w0,w1,w2,...wk]
    Output are lists which have final combined terms and their dashed binary
    representation.
    """
    n=int(n)
    group=[]
    combine=[]
    m=0
    while m<len(f):
        e1=f[m]
        t=0
        while t<len(s):
            e2=s[t]
            e=0
            ad=copy.deepcopy(a[m])
            bd=copy.deepcopy(b[t])
            count=0
            while e<n:
                if e1[e]==e2[e]:
                    count=count+1
                    e=e+1
                else:
                    dash=e
                    e=e+1
            if count==n-1:
                ap=0
                ip=e1[0:dash]+'-'+e1[dash+1:]
                while ap<len(bd):
                    ad.append(bd[ap])
                    ap=ap+1
                ad.sort()    
                if ad not in combine:
                    combine.append(ad)
                if ip not in group:
                    group.append(ip)
            t=t+1
        m=m+1    
    return group,combine

def minFunc(numVar, stringIn):
    """
    This python function takes function of maximum of 4 variables
    as input and gives the corresponding minimized function(s)
    as the output (minimized using the K-Map methodology),
    considering the case of Don’t Care conditions.

    Input is a string of the format (a0,a1,a2, ...,an) d(d0,d1, ...,dm)
    Output is a string representing the simplified Boolean Expression in
    SOP form.

    No need for checking of invalid inputs.

    Do not include any print statements in the function.
    """
    n=numVar
    mt,dc = stringIn.split(" d")
    mt=list(mt)
    dc=list(dc)
    # Assuming ONLY 1,2,3,4 variables as valid cases!
    if int(n)==4:
        gray_code = ['0000','0001','0010','0011','0100','0101','0110','0111','1000','1001','1010','1011','1100','1101','1110','1111']
    if int(n)==3:
        gray_code=['000','001','010','011','100','101','110','111']
    if int(n)==2:
        gray_code=['00','01','10','11']
    if int(n)==1:
        gray_code=['0','1']
    km = [""]*(2**(int(n)))
    i=0
    while i<len(mt):
        if mt[i].isdigit() and mt[i+1].isdigit()==False:
            km[int(mt[i])]=1
            i=i+1
        elif mt[i].isdigit() and mt[i+1].isdigit():
            no = int( mt[i]+mt[i+1])
            km[no]=1
            i=i+2
        else:
            i=i+1
    d=0
    while d<len(dc):
        if dc[d].isdigit() and dc[d+1].isdigit()==False:
            km[int(dc[d])]='d'
            d=d+1
        elif dc[d].isdigit() and dc[d+1].isdigit():
            no = int( dc[d]+dc[d+1])
            km[no]='d'
            d=d+2
        else:
            d=d+1
    z=0
    while z<2**int(n):
        if km[z]=="":
            km[z]=0
            z=z+1
        else:
            z=z+1
    ck=0
    countx=0
    count1=0
    while ck<len(km):
        if km[ck]=='X':
            countx=countx+1
        if km[ck]==1:
            count1=count1+1
        ck=ck+1
    if countx+count1 == 2**int(n):
        if count1>0:
            return 1
    if count1==0:
        return 0
    e=0
    #t=0
    # minterm stores terms which are either 1 or don't care
    # minterm_val stores binary represenation of minterm
    minterm=[]
    minterm_val=[]
    onlyone=[]
    o=0
    while e < len(km): 
        if km[e]==1 or km[e]=='d':
            minterm.append(e)
            minterm_val.append(gray_code[e])
            #t=t+1
            e=e+1
        else:
            e=e+1
    while o<len(km):
        if km[o]==1:
            onlyone.append(o)
            o=o+1
        else:
            o=o+1      
    p,q,r,s,t,g=0,0,0,0,0,0
    set0=[]
    set0_val=[]
    set1=[]
    set1_val=[]
    set2=[]
    set2_val=[]
    set3=[]
    set3_val=[]
    set4=[]
    set4_val=[]
    # set0 is a list which have terms whose binary representation have no 1's
    # set0_val have binary representation of corresponding element in set0
    # set1 is a list which have terms whose binary representation have one 1's
    # set2 is a list which have terms whose binary representation have two 1's
    # set3 is a list which have terms whose binary representation have three 1's
    # set4 is a list which have terms whose binary representation have four 1's
    while p< len(minterm):
        if minterm_val[p] == '0000' or minterm_val[p] == '000' or minterm_val[p] == '00' or minterm_val[p]=='0':
            set0.append(minterm[p])
            set0_val.append(minterm_val[p])
            g=g+1
        if minterm_val[p]=='0001' or minterm_val[p]=='0010' or minterm_val[p]=='0100' or minterm_val[p]=='1000' or minterm_val[p] == '001' or minterm_val[p]=='1' or minterm_val[p] == '010' or minterm_val[p] == '100' or minterm_val[p] == '01' or minterm_val[p] == '10':          
            set1.append(minterm[p])
            set1_val.append(minterm_val[p])
            q=q+1
        if minterm_val[p]=='0011' or minterm_val[p]=='0110' or minterm_val[p]=='1100' or minterm_val[p]=='0101' or minterm_val[p]=='1010' or minterm_val[p]=='1001' or minterm_val[p] == '011' or minterm_val[p] == '101' or minterm_val[p] == '110' or minterm_val[p] == '11':
            set2.append(minterm[p])
            set2_val.append(minterm_val[p])
            r=r+1
        if minterm_val[p]=='0111' or minterm_val[p] == '111' or minterm_val[p]=='1110' or minterm_val[p]=='1101' or minterm_val[p]=='1011':
            set3.append(minterm[p])
            set3_val.append(minterm_val[p])
            s=s+1
        if minterm_val[p]=='1111':
            set4.append(minterm[p])
            set4_val.append(minterm_val[p])
            t=t+1
        p=p+1
    # Tcombine1 have elements which can be combined from set0 and set1 according to Quine McCluskey Algorithm
    # Similarly for all other variables
    Tgroup1,Tcombine1=check(int(n),set0_val,set1_val,set0,set1)
    Tg1,Tc1=copy.deepcopy(Tgroup1),copy.deepcopy(Tcombine1)
    Tgroup2,Tcombine2=check(int(n),set1_val,set2_val,set1,set2)
    Tg2,Tc2=copy.deepcopy(Tgroup2),copy.deepcopy(Tcombine2)
    Tgroup3,Tcombine3=check(int(n),set2_val,set3_val,set2,set3)
    Tg3,Tc3=copy.deepcopy(Tgroup3),copy.deepcopy(Tcombine3) 
    Tgroup4,Tcombine4=check(int(n),set3_val,set4_val,set3,set4)
    Tg4,Tc4=copy.deepcopy(Tgroup4),copy.deepcopy(Tcombine4)
    Fgroup1,Fcombine1=check1(int(n),Tgroup1,Tgroup2,Tcombine1,Tcombine2)
    Fg1,Fc1=copy.deepcopy(Fgroup1),copy.deepcopy(Fcombine1)
    Fgroup2,Fcombine2=check1(int(n),Tgroup2,Tgroup3,Tcombine2,Tcombine3)
    Fg2,Fc2=copy.deepcopy(Fgroup2),copy.deepcopy(Fcombine2)
    Fgroup3,Fcombine3=check1(int(n),Tgroup3,Tgroup4,Tcombine3,Tcombine4)
    Fg3,Fc3=copy.deepcopy(Fgroup3),copy.deepcopy(Fcombine3)
    Egroup1,Ecombine1=check1(int(n),Fgroup1,Fgroup2,Fcombine1,Fcombine2)
    Eg1,Ec1=copy.deepcopy(Egroup1),copy.deepcopy(Ecombine1)
    Egroup2,Ecombine2=check1(int(n),Fgroup2,Fgroup3,Fcombine2,Fcombine3)
    Eg2,Ec2=copy.deepcopy(Egroup2),copy.deepcopy(Ecombine2)
    Sgroup1,Scombine1=check1(int(n),Egroup1,Egroup2,Ecombine1,Ecombine2)
    Sg1,Sc1=copy.deepcopy(Sgroup1),copy.deepcopy(Scombine1)
    Acombine=[Tc1,Tc2,Tc3,Tc4,Fc1,Fc2,Fc3,Ec1,Ec2,Sc1]
    Agroup=[Tg1,Tg2,Tg3,Tg4,Fg1,Fg2,Fg3,Eg1,Eg2,Sg1]
    addth=[]
    resti=minterm
    primei=[]
    if len(Scombine1) != 0:
        return '1'
    else:
        # Finding the list of EPI and the PI which have to be included in the answer
        rest1,prime1=pi(minterm,Ec2,resti,primei)
        rest2,prime2=pi(rest1,Ec1,rest1,prime1)
        rest3,prime3=pi(rest2,Fc3,rest2,prime2)
        rest4,prime4=pi(rest3,Fc2,rest3,prime3)
        rest5,prime5=pi(rest4,Fc1,rest4,prime4)
        rest6,prime6=pi(rest5,Tc4,rest5,prime5)
        rest7,prime7=pi(rest6,Tc3,rest6,prime6)
        rest8,prime8=pi(rest7,Tc2,rest7,prime7)
        rest9,prime9=pi(rest8,Tc1,rest8,prime8)
    finalpi=prime9    
    if len(rest9)!=0:
        # len(rest9)!=0 means there are elements in the minterm list which is not included in any epi so have to be added alone
        ne=0
        while ne<len(rest9):
            finalpi.append([rest9[ne]])
            addth.append(rest9[ne])
            ne=ne+1
        vari=0
        while vari<len(addth):
            Acombine.append([[addth[vari]]])
            vari=vari+1
            addth_val=[]
        vl=0
        while vl<len(addth):
            cd=addth[vl]
            tad=gray_code[cd]
            addth_val.append(tad)
            vl=vl+1
        vb=0
        while vb<len(addth_val):
            Agroup.append([addth_val[vb]])
            vb=vb+1       
    ANSWER=EPI(onlyone,finalpi)
    # Finding the dashed binary representation of the combined terms
    FINAL=[]
    fh=0
    while fh<len(ANSWER):
        al=0
        while al<len(Acombine):
            if ANSWER[fh] not in Acombine[al]:
                al=al+1
            else:
                idx=Acombine[al].index(ANSWER[fh])
                ta=Agroup[al][idx]
                FINAL.append(ta)
                al=al+1
        fh=fh+1   
    # Getting the the final list of terms which will be included in the answer
    fidx=0
    # Sorting the list to get the final answer in lexographical order    
    FINAL.sort(reverse=True)
    alp=[]
    while fidx<len(FINAL):
        alp.append(convert(n,FINAL[fidx]))
        fidx=fidx+1    
    # Concatenating all the terms of the final simplified Boolean expression    
    answer=""
    aw=0
    while aw<len(alp):
        answer=answer + '+' + alp[aw]
        aw=aw+1    
    stringOut=answer[1:]
    return stringOut

