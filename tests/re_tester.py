import re

def main():

    line = 'Modivcare Transportation Provider Network\nG & G MEDICAL TRANSPORT LLC\nTrips for Wednesday, January 3, 2024\n1/4/2024 9:16:10 PM                1 of 25\n'
    # los = re.match(r'LOS: \w{0,3}', line)
    # print(los)
    # miles = re.search(r'Miles: (0|[1-9]\d*)(\.\d+)?', line)
    # print(miles)

    split_lines = line.split('\n')
    print(split_lines)

    # pu = re.match(r'[0-9][0-9]:[0-9][0-9]', line)
    # print(pu.group(0))


if __name__ == '__main__':
    main()