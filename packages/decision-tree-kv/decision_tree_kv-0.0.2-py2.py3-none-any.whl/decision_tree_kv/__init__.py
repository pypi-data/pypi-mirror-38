from typing import List, Dict, Tuple, Union, Any, NewType, Callable
from math import log
from PIL import Image, ImageDraw

STD_LIST_ITEM = NewType('STD_LIST_ITEM', List[Union[str, int, float]])
STD_LIST = NewType('STD_LIST', List[STD_LIST_ITEM])

VERSION = '0.0.2'

#
# base
#

class decisionnode:
    '''class for node in decision tree'''
    def __init__(
        self,
        col: int =-1,
        value: Union[str, int, float, None] = None,
        results: Union[None, Dict[str, int]] = None,
        tb: Any = None,
        fb: Any = None
    ) -> None:
        '''
        col – column from dataset.
        value - value for data in column.
        results - Dict of result. It will be None, if node has 'value'
        tb - decisionnode instance. the way if column's value equal True
        fb - decisionnode instance. the way if column's value equal False
        '''
        self.col = col
        self.value = value
        self.results = results
        self.tb = tb
        self.fb = fb


def divideset(
    rows: STD_LIST,
    column: int,
    value: Union[int, float, str]
  ) -> Tuple[STD_LIST, STD_LIST]:
    '''
    CART (Classification and Regression Trees)
    divide data-set by column to two subsets.
    value can be int, float, str.
    '''
    split_function: Callable[[STD_LIST_ITEM],bool]
    if isinstance(value, int) or isinstance(value, float):
        split_function = lambda row : row[column] >= value
    else:
        split_function = lambda row : row[column] == value

    set1: STD_LIST = [row for row in rows if split_function(row)]
    set2: STD_LIST = [row for row in rows if not split_function(row)]
    return (set1, set2)

def uniquecounts(
    rows: STD_LIST,
    last_row=True
  ) -> Dict[Union[str, int, float], int]:
    '''
    return unique counts.
    result must be in last column
    '''
    results: Dict[Union[str, int, float], int] = {}
    for row in rows:
        if last_row == True:
          r = row[len(row)-1]
        else:
          r = row[0]
        if r not in results:
            results[r] = 0
        results[r] += 1
    return results

def variance(rows: STD_LIST, last_row=True) -> float:
    '''
    calculation for number, not for categories
    '''
    if len(rows)==0:
        return 0.0
    data: List[float]
    if last_row==True:
      data = [float(row[len(row)-1]) for row in rows]
    else:
      data = [float(row[0]) for row in rows]
    mean: float = sum(data)/len(data)
    variance: float = sum([(d-mean)**2 for d in data])/len(data)
    return variance


def giniimpurity(rows: STD_LIST) -> float:
    '''
    calculate Gini impurity
    returns 0 if all is fine
    '''
    total = len(rows)
    counts = uniquecounts(rows)
    imp: float = 0.0
    for k1 in counts:
        p1 = float(counts[k1])/total
        for k2 in counts:
            if k1 == k2:
                continue
            p2 = float(counts[k2])/total
            imp += p1*p2
    return imp


def entropy(rows: STD_LIST) -> float:
    '''
    the function calculate Entropy as sum of p(x) x log(p(x))
    returns 0 if all is fine
    '''
    log2: Callable[[Union[int, float]], float]
    log2 = lambda x: log(x)/log(2)
    results = uniquecounts(rows)

    ent: float = 0.0
    for r in results.keys():
        p = float(results[r])/len(rows)
        ent = ent-p*log2(p)
    return ent


def buildtree(
      rows: STD_LIST,
      scoref: Callable[[STD_LIST],float] = entropy
    ) -> decisionnode:
    '''
    build decition tree
    '''
    if len(rows) == 0:
        return decisionnode()
    current_score: float = scoref(rows)
    # variables for choosing better decision
    best_gain: float = 0.0
    best_criteria = None
    best_sets = None
    column_count: int = len(rows[0])-1
    for col in range(0, column_count):
        column_values = {}
        for row in rows:
            column_values[row[col]] = 1
        for value in column_values.keys():
            (set1, set2) = divideset(rows, col, value)
            p = float(len(set1))/len(rows)
            gain = current_score-p*scoref(set1)-(1-p)*scoref(set2)
            if gain > best_gain and len(set1) > 0 and len(set2) > 0:
                best_gain = gain
                best_criteria = (col, value)
                best_sets = (set1, set2)
    # create sub-branches
    if best_gain > 0:
        trueBranch: decisionnode = buildtree(best_sets[0])
        falseBranch: decisionnode = buildtree(best_sets[1])
        return decisionnode(col=best_criteria[0], value=best_criteria[1],
                            tb=trueBranch, fb=falseBranch)
    else:
        return decisionnode(results=uniquecounts(rows))

#
# print tree
#


def printtree(tree: decisionnode, indent: str = '') -> None:
    '''print tree to console'''
    if tree.results != None:
        print(str(tree.results))
    else:
        # print contion
        if isinstance(tree.value, int) or isinstance(tree.value, float):
            print('column['+str(tree.col)+']: >= "'+str(tree.value)+'"? ')
        else:
            print('column['+str(tree.col)+']: == "'+str(tree.value)+'"? ')
        # print branches
        print(indent+'True -> ', end='')
        printtree(tree.tb, indent+' ')
        print(indent+'False -> ', end='')
        printtree(tree.fb, indent+' ')
    return None


def tree_to_str(tree: decisionnode, indent: str = '') -> str:
    '''print tree to string'''
    main_string: str = ''
    if tree.results != None:
        main_string += str(tree.results)
        main_string += "\n"
    else:
        if isinstance(tree.value, int) or isinstance(tree.value, float):
            s: str = 'column['+str(tree.col)+']: >= "'+str(tree.value)+'"? '
            main_string += s
            main_string += "\n"
        else:
            s: str = 'column['+str(tree.col)+']: == "'+str(tree.value)+'"? '
            main_string += s
            main_string += "\n"
        main_string += indent+'True -> '
        main_string += tree_to_str(tree.tb, indent+' ')
        main_string += indent+'False -> '
        main_string += tree_to_str(tree.fb, indent+' ')
    return main_string


#
# draw tree as a picture
#

def getwidth(tree: decisionnode) -> int:
    if tree.tb == None and tree.fb == None:
        return 1
    return getwidth(tree.tb)+getwidth(tree.fb)


def getdepth(tree: decisionnode) -> int:
    if tree.tb == None and tree.fb == None:
        return 0
    return max(getdepth(tree.tb), getdepth(tree.fb))+1

def drawnode(draw: ImageDraw, tree: decisionnode, x: int, y: int) -> None:
    if tree.results==None:
        # calculate width
        w1=getwidth(tree.fb)*100
        w2=getwidth(tree.tb)*100
        # calculate space
        left=x-(w1+w2)/2
        right=x+(w1+w2)/2
        # lable with condition
        draw.text((x-20,y-10),str(tree.col)+':'+str(tree.value),(0,0,0))
        # draw lines
        draw.line((x,y,left+w1/2,y+100),fill=(255,0,0))
        draw.line((x,y,right-w2/2,y+100),fill=(255,0,0))
        # draw nodes
        drawnode(draw,tree.fb,left+w1/2,y+100)
        drawnode(draw,tree.tb,right-w2/2,y+100)
    else:
      txt=' \n'.join(['%s:%d'%v for v in tree.results.items( )])
      draw.text((x-20,y),txt,(0,0,0))
      return None

def drawtree(tree: decisionnode, jpeg: str ='tree.jpg') -> None:
    w=getwidth(tree)*100
    h=getdepth(tree)*100+120
    img=Image.new('RGB',(w,h),(255,255,255))
    draw=ImageDraw.Draw(img)
    drawnode(draw,tree,w/2,20)
    img.save(jpeg,'JPEG')
    img.show('decision tree image')
    return None

def showtree(tree: decisionnode) -> None:
    w=getwidth(tree)*100
    h=getdepth(tree)*100+120
    img=Image.new('RGB',(w,h),(255,255,255))
    draw=ImageDraw.Draw(img)
    drawnode(draw,tree,w/2,20)
    img.show('decision tree image')
    return None


#
# classification
#


def classify(
    observation: List[Union[str, int, float]],
    tree: decisionnode
) -> Dict[str, int]:
    '''
    the function traverses tree as printtree
    '''
    if tree.results != None:
        return tree.results
    else:
        v: Union[str, int, float] = observation[tree.col]
        branch = None
        if isinstance(v, int) or isinstance(v, float):
            if v>=tree.value:
                branch=tree.tb
            else:
                branch=tree.fb
        else:
          if v==tree.value:
              branch=tree.tb
          else:
              branch=tree.fb
        return classify(observation,branch)

def mdclassify(observation,tree: decisionnode) -> Dict[str, int]:
    '''good for None values'''
    if tree.results!=None:
        return tree.results
    else:
        v=observation[tree.col]
        if v==None:
          # take None value
          tr,fr=mdclassify(observation,tree.tb),mdclassify(observation,tree.fb)
          tcount=sum(tr.values())
          fcount=sum(fr.values())
          tw=float(tcount)/(tcount+fcount)
          fw=float(fcount)/(tcount+fcount)
          result={}
          for k,v in tr.items( ):
              result[k]=v*tw
          for k,v in fr.items( ):
            result[k]=v*fw
          return result
        else:
            if isinstance(v,int) or isinstance(v,float):
                if v>=tree.value:
                    branch=tree.tb
                else:
                    branch=tree.fb
            else:
                if v==tree.value:
                    branch=tree.tb
                else:
                    branch=tree.fb
            return mdclassify(observation,branch)