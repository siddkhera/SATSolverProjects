import pycosat
from csv import reader
from itertools import combinations

with open('slitherlink.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    squares = list(csv_reader)

rows=len(squares) #No. of Rows
cols=len(squares[0]) #No. of Coloumns

def LineID(x,y,horizontal):
    return ((0<=x<=rows and 0<=y<cols) and ((x*cols)+y+1)) if horizontal else ((0<=x<rows and 0<=y<=cols) and cols*(rows+x+1)+x+y+1)

def linesAround(x,y,horizontal,pre):
    return list(filter((False).__ne__, ([LineID(x,y,False), LineID(x-1,y,False), LineID(x,y-1,True)] if pre else [LineID(x,y+1,False), LineID(x-1,y+1,False), LineID(x,y+1,True)]) if horizontal else ([LineID(x,y-1,True), LineID(x,y,True), LineID(x-1,y,False)] if pre else [LineID(x+1,y-1,True), LineID(x+1,y,True), LineID(x+1,y,False)])))

def nTrue(vars,n):
    return list(map(lambda x:list(x),list(combinations([-i for i in vars],n+1))))+list(map(lambda x:list(x),list(combinations(vars,len(vars)+1-n))))

def aroundSquare(x,y):
    return [LineID(x,y,True),LineID(x,y,False),LineID(x+1,y,True),LineID(x,y+1,False)]

cnf=[]

for i in list(range(rows+1)):
    for j in list(range(cols+1)):
        cnf+=nTrue(aroundSquare(i,j),int(squares[i][j])) if (i<rows and j<cols and squares[i][j]!='.') else []
        for hori in [True,False]:
            for t in [True,False]:
                cnf+=[k+[-LineID(i,j,hori)] for k in nTrue(linesAround(i,j,hori,t),1)] if ((not hori or j<cols) and (hori or i<rows)) else []

def IdLinesAround(num):
        return linesAround((num-((rows+1)*cols+1))//(cols+1),(num-((rows+1)*cols+1))%(cols+1),False,True)+linesAround((num-((rows+1)*cols+1))//(cols+1),(num-((rows+1)*cols+1))%(cols+1),False,False) if num>(rows+1)*cols else linesAround((num-1)//(cols),(num-1)%(cols),True,True)+linesAround((num-1)//(cols),(num-1)%(cols),True,False)

def OneLoop(TrueLines,LinesNotTravelled):
    while(LinesNotTravelled!=[]):
        TrueLines.remove(LinesNotTravelled[0])
        LinesNotTravelled=[i for i in IdLinesAround(LinesNotTravelled[0]) if (i in TrueLines)]
    return (TrueLines==[])

for sol in pycosat.itersolve(cnf):
    TrueLines=[i for i in sol if i>0]
    if OneLoop(TrueLines,[TrueLines[0]]):
        print(sol)
