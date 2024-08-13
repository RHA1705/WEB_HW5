import argparse
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='Enter your name')
    parser.add_argument('age', help='Enter your age')

    args = parser.parse_args()

    try:
        n = int(args.name)
        if n:
            print("Name can't be a number")
            sys.exit(1)
    except ValueError:
        pass

    print(f'Hello, {args.name}!')
    if args.age:
        print(f'You are {args.age} years old.')

if __name__ == '__main__':
    main()
