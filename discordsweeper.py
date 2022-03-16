import random


def printDiscordGrid(grid, width, height):
  ss = ""
  for y in range(height):
    s = ""
    for c in grid[y]:
      cc = ""
      if c == 'b': cc = "||:bomb:||"
      if c == '1': cc = "||:one:||"
      if c == '2': cc = "||:two:||"
      if c == '3': cc = "||:three:||"
      if c == '4': cc = "||:four:||"
      if c == '5': cc = "||:five:||"
      if c == '6': cc = "||:six:||"
      if c == '7': cc = "||:seven:||"
      if c == '8': cc = "||:eight:||"
      if cc == "": cc = "||:blue_square:||"
      s += cc
    ss += s + "\n"
  return ss

def placeMines(grid, width, height,  n):
  while n > 0:
    y = random.randint(0,height-1)
    x = random.randint(0,width-1)
    if grid[y][x] != 'b':
      grid[y][x] = 'b'
      n -= 1

def setNums(grid, width, height):
  for y in range(height):
    for x in range(width):
      if grid[y][x] == 'b': continue
      n = 0
      if y > 0 and grid[y-1][x] == 'b': n += 1
      if y < height-1 and grid[y+1][x] == 'b': n += 1
      if x > 0 and grid[y][x-1] == 'b': n += 1
      if x < width-1 and grid[y][x+1] == 'b': n += 1

      if y > 0 and x > 0 and grid[y-1][x-1] == 'b': n += 1
      if y > 0 and x < width-1 and grid[y-1][x+1] == 'b': n += 1
      if y < height-1 and x > 0 and grid[y+1][x-1] == 'b': n += 1
      if y < height-1 and x < width-1 and grid[y+1][x+1] == 'b': n += 1

      if n == 0: continue
      grid[y][x] = str(n)


def makeDiscordMinesweeper(width, height, mines):
    grid = [ [ ' ' for i in range(width) ] for j in range(height) ]
    placeMines(grid, width, height, mines)
    setNums(grid, width, height)
    return printDiscordGrid(grid, width, height)



if __name__ == "__main__":
    print(makeDiscordMinesweeper(7, 7, 7))
