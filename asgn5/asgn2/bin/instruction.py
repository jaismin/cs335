from assemblygen import *
import globalvars as g

#Breaks string representation of array to array name and index
#if not array returns (Variable name,None)
def varname(var):
    if(isInt(var)):
        return var,None
    elif(var.find("[")!=-1):
        n=var.find("[")
        m=var.find("]")
        index=var[n+1:m]
        # g.variables.append(("v_"+var[0:n],1))     //arrays are declared using special command declare
        return "v_"+var[0:n],index
    else:
        g.variables.append(("v_"+var,0))
        return "v_"+var,None

class instruction(object):
    # convert each line of code to an object instruction class
    # also finds basicblocks and labels 
    def convert(self, param):
        # print(param)
        if(len(param)==1):
            return 0
        self.lineno=param[0]
        self.op=param[1]
        # print(param)
        if (param[1]=="ifgoto"):
            self.jmp=True
            self.cmpl=True
            self.cmpltype=param[2]
            self.src1,self.src1index=varname(param[3])
            self.src2,self.src2index=varname(param[4])
            self.jlno=param[5]
            g.basicblock.append(int(self.lineno))
            # g.basicblock.append(int(self.jlno)-1)
            # g.splitins[i].jlno
            # g.marker.append(int(self.jlno)-1)
        elif(param[1]=="goto"):
            self.jmp=True
            self.jlno="l_"+param[2]
            g.basicblock.append(int(self.lineno))
        elif (param[1]=="call"):
            g.basicblock.append(int(self.lineno))
            if(int(self.lineno)<=len(g.splitins)):
                g.basicblock.append(int(self.lineno)+1)
            self.func=True
            self.funcname="u_"+param[2]
        elif (param[1]=="ret"):
            g.debug("instruction.py :: ret"+str(param))
            if(len(param)==3):
                self.dst,self.dstindex=varname(param[2])
            else:
                self.dst=None
            self.returnc=True
        elif (param[1]=="func"):
            # print("i m here")
            # g.basicblock.append(int(self.lineno))
            g.marker.append(int(self.lineno)-1)
            for i in range(3,len(param)):
                self.paramlist.append(varname(param[i]))
            self.lbl=True
            self.lblname="u_"+param[2]
        elif (param[1]=="label"):
            # print("i m here")
            g.basicblock.append(int(self.lineno)-1)
            g.marker.append(int(self.lineno)-1)
            self.lbl=False
            self.lblname="l_"+param[2]
        elif (param[1]=="print"):
            g.debug("printer")
            self.printc=True
            self.paramlist =[]
            g.printstrings.append(["str_"+str(self.lineno),str(param[2][:-1]+"\\n\\0\"")])
            self.paramlist.append("$str_"+str(self.lineno))
            # g.debug("len of param :: "+str(len(param)))
            for i in range(3,len(param)):
                temp,tempindex=varname(param[i])
                self.paramlist.append([temp,tempindex])
            g.debug("print line :: "+str(self.paramlist))
            g.debug("string line :: "+str(g.printstrings))
            # self.src1,self.src1index=varname(param[2])
        elif (param[1]=="input"):
            self.inputc=True
            self.src1,self.src1index=varname(param[2])
        elif (param[1]=="=" or param[1]=='not'):
            self.dst,self.dstindex=varname(param[2])
            self.src1,self.src1index=varname(param[3])
            # g.variables.append(varname(param[2]))
            # g.variables.append(varname(param[3]))
        elif (param[1]=="push" or param[1]=="pop"):
            self.dst,self.dstindex=varname(param[2])
        elif (param[1]=="declare"):
            g.variables.append(("v_"+param[2],param[3]))
        else:
            # print(param)
            self.dst,self.dstindex=varname(param[2])
            self.src1,self.src1index=varname(param[3])
            self.src2,self.src2index=varname(param[4])
            # g.variables.append(varname(param[2]))
            # g.variables.append(varname(param[3]))
            # g.variables.append(varname(param[4]))
    # prints an object of this class
    # Only for debugging purposes
    def printobj(self):
       g.debug("line no: "+self.lineno)
       g.debug("op: "+self.op)
       g.debug("dst: "+str(self.dst))
       g.debug("src1: "+str(self.src1))
       g.debug("src2: "+str(self.src2))
       g.debug("jmp: "+str(self.jmp))
       g.debug("cmpl: "+str(self.cmpl))
       g.debug("cmpltype: "+str(self.cmpltype))
       g.debug("jlno: "+str(self.jlno))
       g.debug("lbl: "+str(self.lbl))
       g.debug("lblname: "+str(self.lblname))
       g.debug("func: "+str(self.func))
       g.debug("funcname: "+str(self.funcname))
       g.debug("print: "+str(self.printc))
       g.debug("input: "+str(self.inputc))
       g.debug("return: "+str(self.returnc))
       g.debug("\n")
    # Used for initialisation
    def __init__(self):
        self.lineno=0
        self.op=None             #operator
        self.dst=None            #destination
        self.dstindex=None       #Only for Array
        self.src1=None           #source1
        self.src1index=None      #Only For Array   
        self.src2=None           #source2
        self.src2index=None      #Only For Array
        self.jmp=False           #if jump or not
        self.cmpl=False          #if compare or not
        self.cmpltype=None
        self.jlno=0              #line number to jump to
        self.lbl=False           #label of a function
        self.lblname=None        #Name of label
        self.func=False
        self.funcname=None
        self.printc=False        #If we have to print or not(lib func)
        self.inputc=False        #If we have to take input or not(lib func)
        self.returnc=False       #If we have to return or not(lib func)
        self.paramlist=[]
