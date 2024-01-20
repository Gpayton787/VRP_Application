import re

def main():

    line = 'LOS: W   M W F     CPay: $0.00 PCA: 0  AEsc: 0  CEsc: 0  Seats: 0  Miles: 100.05'
    los = re.match(r'LOS: \w{0,3}', line)
    print(los)
    miles = re.search(r'Miles: (0|[1-9]\d*)(\.\d+)?', line)
    print(miles)

    # split_lines = line.split(' ')
    # re_split = re.split(r' {3,}', line)
    # print(split_lines)
    # print(re_split)

    # pu = re.match(r'[0-9][0-9]:[0-9][0-9]', line)
    # print(pu.group(0))


if __name__ == '__main__':
    main()