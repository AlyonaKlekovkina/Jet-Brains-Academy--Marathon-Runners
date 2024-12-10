import os
import requests
import sys

if __name__ == '__main__':
    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if 'data_about_marathon_runners.txt' not in os.listdir('../Data'):
        sys.stderr.write("[INFO] Dataset is loading.\n")
        url = "https://www.dropbox.com/s/xmsobyv41wz8vb4/data_about_marathon_runners.txt?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/data_about_marathon_runners.txt', 'wb').write(r.content)
        sys.stderr.write("[INFO] Loaded.\n")

    # write your code here
    raw_data_from_file = open('../Data/data_about_marathon_runners.txt', 'r')
    big_list = []
    for line in raw_data_from_file:
        symbol = line.split(',')
        clean_list = []
        for i in symbol:
            if '\n' not in i and '\t' not in i:
                clean_list.append(i)
            elif '\n' in i:
                clean_info = i.split('\n')
                clean_list.append(clean_info[0])
            elif '\t' in i:
                clean_info = i.split('\t')
                clean_list.append(clean_info[0])
        big_list.append(clean_list)
    print(big_list)
