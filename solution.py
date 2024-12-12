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
    nested_list = []
    for line in raw_data_from_file:
        symbol = line.split(',')
        processed_info = []
        for i in symbol:
            if '\n' not in i and '\t' not in i:
                processed_info.append(i)
            elif '\n' in i:
                clean_info = i.split('\n')
                processed_info.append(clean_info[0])
            elif '\t' in i:
                clean_info = i.split('\t')
                processed_info.append(clean_info[0])
        nested_list.append(processed_info)

    updated_nl = []
    activity_list = []
    for j in nested_list:
        updated_info = []
        for k in range(len(j) - 1):
            if j[k] == 'Yes':
                updated_info.append(1)
            elif j[k] == 'No':
                updated_info.append(0)
            else:
                converted = float(j[k])
                if converted.is_integer():
                    updated_info.append(int(converted))
                else:
                    updated_info.append(converted)
        activity_key = j[-1]
        if activity_key not in activity_list:
            activity_list.append(activity_key)
        updated_info.append(activity_key)
        updated_nl.append(updated_info)

    sorted_activity_list = sorted(activity_list)
    vector_dictionary = {}
    nes_list = []
    for m in range(len(activity_list)):
        l = []
        for n in range(len(activity_list)):
            if m == n:
                l.append(1)
            else:
             l.append(0)
        vector_dictionary.update({sorted_activity_list[m] : l})
        nes_list.append(l)

    final_nested_list = []
    y_train = []
    for i in updated_nl:
        x_train = []
        for j in range(len(i)):
            if j == 0:
                y_train.append(i[j])
            if j == len(i) - 1:
                vector_list = vector_dictionary.get(i[j])
                for b in vector_list:
                    x_train.append(b)
            elif (j != 0) and (j != len(i) - 1):
                x_train.append(i[j])
        final_nested_list.append(x_train)

    print(y_train)
    print(final_nested_list)



