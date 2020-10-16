import time
import sys
import copy

lookup = {}
boxes = {}
cs = [set()]*27
symbols = ["0","1","2","3","4","5","6","7","8","9"]

def main():
   file1 = open("sudoku_puzzles_1.txt", "r")
   start = time.time()
   count = 0
     
   pzlSide = int(.5 + 81**.5)
   box1 = int(.5 + pzlSide**.5)
   box2 = int(.5 + pzlSide**.5)
   global lookup
   global boxes
   global cs
   
   while box1 * box2 != pzlSide:
      if box1 * box2 < pzlSide:
         box2+=1
      elif box1 * box2 > pzlSide:
         box+=-1
   boxHeight = min(box1, box2)
   boxWidth = min(box1, box2)
   for x in range(pzlSide*3):
      cs[x] = set()
   
   for x in range (81):
      row = int(x/pzlSide)
      col = x%pzlSide
      box = int(col / boxWidth) + int(pzlSide / boxWidth) * int(row / boxHeight)
      lookupSet = set()
      tuple =(row,col,box)
      
      for z in range(tuple[1], (tuple[1]+9*8)+1, 9):
         lookupSet.add(z)
      for y in range(tuple[0] * 9, tuple[0] * 9 + 9):
         lookupSet.add(y)
         
      cs[box].add(x)
      cs[row+pzlSide].add(x)
      cs[col+2*pzlSide].add(x)
      lookup[x] = lookupSet
      
   for x in range(81):
      row = int(x/pzlSide)
      col = x%pzlSide
      box = int(col / boxWidth) + int(pzlSide / boxWidth) * int(row / boxHeight)
      for element in cs[box]:
         lookup[x].add(element)
      lookup[x].remove(x) 

   numSet = {1,2,3,4,5,6,7,8,9}
   for line in file1:
      neighborsFilled = {}
      count+=1
      input = line[:-1]
      for x in range(81):
         if input[x]==".":
            neighbors = set();
            for num in lookup[x]:
               if input[num]!=".":
                  neighbors.add(int(input[num]))
            newSet = numSet-neighbors
            neighborsFilled[x] = newSet
       
      symbolsFilled = [{char:set() for char in numSet}]*27
      #print(symbolsFilled)
      for cSet in list(enumerate(cs)):
         for char in numSet:
            for pos in cSet[1]:
               if input[pos]==".":
                  if char in neighborsFilled[pos]:
                     symbolsFilled[cSet[0]][char].add(pos)
                              
      solution = bruteForce(input,neighborsFilled)
      if solution == "":
         print(count,"No solution", time.time() - start)
      else:
         print(count, solution,time.time() - start)
      
def bruteForce(pzl, newNeighbors):   
   neighborsFilled = {}  
 
   for key in newNeighbors:
      neighborsFilled[key] = newNeighbors[key].copy()

   delList = []
   for key in neighborsFilled:
      if len(neighborsFilled[key])==0:
         return ""
      if len(neighborsFilled[key])==1:
         delList.append(key)
         sym  = neighborsFilled[key].pop()
         pzl = pzl[:key] + symbols[sym] + pzl[key+1:]
         for val in lookup[key]:
            if val in neighborsFilled:
               if sym in neighborsFilled[val]:            
                  neighborsFilled[val].remove(sym)
               
   for num in delList:
      del neighborsFilled[num]
   
   if isSolved(neighborsFilled):
      return pzl
   delList = []
   #print(symbolsFilled)
   for cSet in list(enumerate(cs)):
      symbolsFilled = {x:set() for x in range(1,10)}
      for char in {1,2,3,4,5,6,7,8,9}:         
         for pos in cSet[1]:
            if pzl[pos]==".":
               if char in neighborsFilled[pos]:
                  symbolsFilled[char].add(pos)
         if len(symbolsFilled[char])==1:
            num = symbolsFilled[char].pop()
            pzl = pzl[:num] + symbols[char] +  pzl[num+1:]
            for val in lookup[num]:
               if val in neighborsFilled:
                  if char in neighborsFilled[val]:            
                     neighborsFilled[val].remove(char)
            delList.append(num)
            
   for num in delList:
      del neighborsFilled[num]
                       
   if isSolved(neighborsFilled):
      return pzl
                   
   minIndex = 0
   minValue = 100
   for key in neighborsFilled:
      if len(neighborsFilled[key]) < minValue:
         minIndex = key
         minValue = len(neighborsFilled[key])
      
      if minValue==1:
         break 
      if minValue==0:
            return ""   
   
   possNums = neighborsFilled[minIndex]  
   nextPos = minIndex
   del neighborsFilled[minIndex]
   for x in possNums: #generalize later
      dict = {}
      for val in lookup[nextPos]:
         if val in neighborsFilled:
            if x in neighborsFilled[val]:            
               neighborsFilled[val].remove(x)
               dict[val] = True
                  
      newPzl = pzl[:nextPos] + symbols[x] + pzl[nextPos+1:]   
      bf = bruteForce(newPzl, neighborsFilled)
      
      if bf != "":
         return bf   
      
      for key in dict:
         if dict[key] == True:
            neighborsFilled[key].add(x)      
   return "" 
      
   
def isSolved(dict):
   if len(dict)==0:
      return True
   return False
main()

# Loop through each CS
#    Loop through each (unset) symbol
#       Loop through each position
#          Loop through each neighbor
# 
# Calculate possiblities for each position
#    Loop through all the neighbors
# 
# Loop through each CS:
#    Make an empty dictionary indexed by symbol, counting the number of times each symbol is possible