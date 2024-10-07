from typing import Literal,Optional
from random import randint

def bubble_sort(array:list[int]) -> list[list[int]]:
    ops = []
    issorted = False
    while not issorted:
        issorted=True
        for i in range(1,len(array)):
            if array[i-1] > array[i]:
                array[i-1],array[i] = array[i],array[i-1]
                ops.append(array.copy())
                issorted=False
    return ops

def insertion_sort(array:list[int]) -> list[list[int]]:
    ops = []
    for i in range(1,len(array)):
        v = array[i]
        j = i - 1
        while j >= 0 and array[j] > v:
            array[j+1] = array[j]
            j -=1
            ops.append(array.copy())
        j += 1
        array[j] = v
        ops.append(array.copy())

    return ops

def selection_sort(array:list[int]) -> list[list[int]]:
    ops = []
    for i in range(len(array)):
        _min = i
        for j in range(i,len(array)):
            if array[j] < array[_min]:
                array[j],array[_min] = array[_min],array[j]
                ops.append(array.copy())
    return ops

def merge_sort(array:list[int]) -> list[list[int]]:
    ops = []
    def merge_sort_rec(array:list[int],s:int,e:int):
        nonlocal ops
        if s >= e:return
        m = (s + e)//2
        merge_sort_rec(array,s,m)
        merge_sort_rec(array,m+1,e)

        i,j = s,m+1
        tmp = []
        while i <= m and j <= e:
            if array[i] < array[j]:
                tmp.append(array[i])
                i+=1
            else:
                tmp.append(array[j])
                j+=1
        
        while i <= m:
            tmp.append(array[i])
            i+=1
        while j <= e:
            tmp.append(array[j])
            j+=1
        
        for i,v in enumerate(tmp):
            array[s + i] = v
            ops.append(array.copy())
    merge_sort_rec(array,0,len(array)-1)
    return ops
MIN_SIZE_SWITCH_SORT_ALGO = 10 # the minimal size of an array, when we switch froma sorting algorithm to another
def hybrid_merge_insertion_sort(array:list[int]) -> list[list[int]]:
    ops = []
    def hmi_rec(array:list[int],s:int,e:int) -> None:
        nonlocal ops
        if s > e or e >= len(array) or s < 0:return 
        if (e - s + 1) <= MIN_SIZE_SWITCH_SORT_ALGO:
            for i in range(s+1,e+1):
                v = array[i]
                j = i - 1
                while j >= s and array[j] > v:
                    array[j+1]=array[j]
                    j-=1
                    ops.append(array.copy())
                j+=1
                array[j]=v
                ops.append(array.copy())
            return
            
        m = (s + e)//2
        hmi_rec(array,s,m)
        hmi_rec(array,m+1,e)

        # merge
        i,j = s,m+1
        tmp = []
        while i <= m and j <= e:
            if array[i] < array[j]:
                tmp.append(array[i])
                i+=1
            else:
                tmp.append(array[j])
                j+=1
        
        for i in range(i,m+1):
            tmp.append(array[i])
        
        for j in range(j,e+1):
            tmp.append(array[j])
        
        for i,v in enumerate(tmp):
            array[s + i] = v
            ops.append(array.copy())
    
    hmi_rec(array,0,len(array)-1)
    
    return ops

def quick_sort(array:list[int]) -> list[list[int]]:
    ops = []
    def pivoting(array:list[int],s:int,e:int) -> int:
        nonlocal ops
        p = e
        e -= 1
        while s < e:
            while s < e and array[s] < array[p]:s += 1
            while s < e and array[e] >= array[p]: e-=1
            if s < e:
                array[s],array[e] = array[e],array[s]
                ops.append(array.copy())
            
        if array[s] < array[p]:
            s += 1
        array[s],array[p] = array[p],array[s]
        ops.append(array.copy())
        return s

    def qs(array:list[int],s:int,e:int) -> None:
        nonlocal ops
        if s < 0 or e >= len(array) or s >= e: return
        p=pivoting(array,s,e)
        qs(array,s,p-1)
        qs(array,p+1,e)
    
    qs(array,0,len(array)-1)
    return ops

def bogo_sort(array:list[int]) -> list[list[int]]:
    ops = []
    def issorted(array:list[int]) -> bool:
        for i in range(1,len(array)):
            if array[i-1] > array[i]:return False
        return True
    while not issorted(array):
        i,j = randint(0,len(array)-1),randint(0,len(array)-1)
        array[i],array[j] = array[j],array[i]
        ops.append(array.copy())
    
    return ops

class Node[T :int|float]:
    def __init__(self,v:T) -> None:
        self.v : T = v
        self.r : Optional[Node[T]] = None
        self.l : Optional[Node[T]] = None
        self.goto:Literal['r','l'] = 'r'

class MaxHeap[T :int|float]:
    def __init__(self) -> None:
        self.root : Optional[Node[T]] = None
    
    def push(self,v:T) -> None:
        if self.root is None:
            self.root = Node(v)
        else:
            parent_node:Node = self.root
            current_node:Optional[Node[T]] = None

            while True:
                if parent_node.v < v:
                    tmp = parent_node.v
                    parent_node.v = v
                    v = tmp
                
                match parent_node.goto:
                    case "l":
                        current_node = parent_node.l
                    case "r":
                        current_node = parent_node.r
                
                parent_node.goto = "r" if parent_node.goto == 'l' else "l"
                
                if current_node is None:
                    match parent_node.goto:
                        case "l":
                            parent_node.r = Node(v)
                        case "r":
                            parent_node.l = Node(v)
                    break
                parent_node = current_node
        
    def pop(self) -> Optional[T]:
        if self.root is None:return None
        v = self.root.v

        prev_node:Optional[Node[T]] = None
        current_node: Node[T]       = self.root
        next_node: Node[T]
        
        while True:
            match current_node.l,current_node.r:
                case None,None:
                    if prev_node is None:
                        self.root = None
                    else:
                        if prev_node.r is current_node:
                            prev_node.r = None
                        elif prev_node.l is current_node:
                            prev_node.l = None
                    break
                    
                case l,r if l is not None and r is not None:
                    next_node = r if r.v > l.v else l
                    current_node.v = max(r.v , l.v)
                
                case l,_ if l is not None:
                    next_node = l
                    current_node.v = l.v
                
                case _,r if r is not None:
                    next_node = r
                    current_node.v = r.v
            
            prev_node = current_node
            current_node = next_node
        return v
    
    def to_list(self) -> list[T]:
        l = []
        x = self.pop()
        while x is not None:
            l.append(x)
            x = self.pop()

        for n in l:
            self.push(n)
        return l

def heap_sort(array:list[int]) -> list[list[int]]:
    ops = [array.copy()]
    mh = MaxHeap[int]()
    for n in array:
        mh.push(n)
        ops.append((mh.to_list()))
    return ops




