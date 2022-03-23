import time
# Build a text_version of Suduku Solver
# temporarily question is input manually
suduku_grid = [ [0,2,0,5,0,7,0,0,0],
                [0,4,0,2,0,8,7,0,1],
                [0,0,0,0,0,1,4,8,0],
                [1,5,0,0,0,0,2,0,0],
                [9,6,0,7,0,2,1,0,0],
                [0,8,0,0,0,6,9,4,0],
                [2,0,6,0,7,0,5,1,4],
                [5,1,8,0,0,4,3,6,0],
                [0,0,7,1,0,0,0,0,9] ]

def vis(grid):
    for i in range(len(grid)):
        #every three rows, print a horizontal line, but not before the first row.
        if i%3 == 0 and i!=0:
            print('- - - - - - - - - - -')
        #evert three cols, print a vertical line, but not before and after the col.
        for j in range(len(grid)):
            if j%3==0 and j!=0:
                print('| ',end="") # end="" means print in the same line
            if j == 8: #change line when reaching the last col.
                print(grid[i][j])
            else: #print in the same line unless reach the last col.
                print(str(grid[i][j]) + ' ',end="")

def next_blank(grid): #simply walk throught the grid to find the blank or 0.
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j]==0:
                pos = (i,j)
                return pos #return (row,col)
    return None #board is filled.

def IsValid(grid, num, row, col):
    #Check row
    for i in range(len(grid[0])):
        if grid[row][i]==num and i!=col: #check through the row, but ignore the one we just filled in.
            return False
    #Check col
    for j in range(len(grid)):
        if grid[j][col]==num and j!=row: #check through the col, but ignore the one we just filled in.
            return False
    #Check the 3*3 Block
    #Determine where the box index is
    #top-left is (0,0), right direction = col-axis, down direction = row-axis
    block_row = row//3
    block_col = col//3
    #loop through the blocks
    for i in range(block_row*3,block_row*3+3): #to get to the right index, need mul by 3
        for j in range(block_col*3,block_col*3+3):
            if grid[i][j] == num and i!=row and j!=col: #check through the block area, but ignore the one we just filled in.
                return False
    return True


def sol(grid,cnt):
#recursive condition
    #recursion ended condition
    next = next_blank(grid)
    if not next: #means can't find the next empty slot to fill in, in other words, grid is fully filled.
        print(cnt)
        return True
    else:
        row,col = next[0],next[1] #not completed yet, returning next blank position.
    for num in range(1,10): #try fill the number into the blank.
        if IsValid(grid, num, row, col): #if it is valid then plug in the value.
            grid[row][col]= num
            cnt += 1
            print(next_blank(suduku_grid))
            print(vis(suduku_grid))
            if sol(grid,cnt): #recursively finding the solution.
                return True
            grid[row][col]=0 #reset the number, waiting for try another one.
    return False

start = time.time()
itr_cnt = 0
sol(suduku_grid,itr_cnt)
end = time.time()
print(end - start)