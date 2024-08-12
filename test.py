import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='Prosty przykład użycia argparse')
    parser.add_argument('-n', '--name', help='Podaj swoje imię')
    parser.add_argument('-a', '--age', help='Podaj swój wiek')

    args = parser.parse_args()
    
    if not args.name:
        print('Argument --name musi być podany przed --age')
        sys.exit(1)
    else:
        print(f'Witaj, {args.name}!')
        if args.age:
            print(f'Masz {args.age} lat.')

if __name__ == '__main__':
    main()