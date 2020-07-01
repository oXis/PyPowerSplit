import base64
import argparse
import sys

def parse(data):

    funcList = ['']
    block = False
    counter = 0

    for line in data:

        if '#' in line:
            i = line.find('#')
            line = line[:i] + '\n'

        if line == '' or line == '\n':
            continue

        if "function " in line[:10]: # /s is important
            block = True
            counter += line.count('{')
            funcList.append(line)
            print("[+] New block", line.strip(), file=sys.stderr)
        elif "filter " in line[:10]: # /s is important
            block = True
            counter += line.count('{')
            funcList.append(line)
            print("[+] New block", line.strip(), file=sys.stderr)
        elif block:
            funcList[-1] += line
            counter += line.count('{')
            counter -= line.count('}')
            if counter == 0:
                block = False
                funcList[-1] = funcList[-1][:-1] # remove last \n
                funcList.append('')
                print("[+] Block end", line.strip(), file=sys.stderr)
        else:
            funcList[-1] += line

    return filter(lambda x: x!= '', funcList)

def main(arg):
    with open(arg.file, 'r') as f:
        data = f.readlines()

    funcList = list(parse(data))

    for item in funcList[:-1]:
        encodedBytes = base64.b64encode(item.encode("utf-8"))
        encodedStr = str(encodedBytes, "utf-8")
        print(encodedStr)

    # stupid hack to remove last \n
    encodedBytes = base64.b64encode(funcList[-1].encode("utf-8"))
    encodedStr = str(encodedBytes, "utf-8")
    print(encodedStr, end='')

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('file',
                        help='Powershell script',
                        action="store",
                        type=str)


    sys.exit(main(parser.parse_args()))
