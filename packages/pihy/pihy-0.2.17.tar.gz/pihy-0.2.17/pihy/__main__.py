import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import x

def main():
  print('foo = ', 1)
  print(x.joke())

if __name__ == '__main__':
  main()
