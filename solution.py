import os
import requests
import sys
import math

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
    def nested_list_nospaces():
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
        return nested_list


    def nested_list_converted_info(nested_list):
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
        return updated_nl, activity_list


    def create_vectordict_prelist(activity_list):
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
        return vector_dictionary, nes_list


    def create_combined_list(updated_nl, vector_dictionary):
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
        return final_nested_list


    def normalize_age_speed_list(final_nested_list, test_vector):
        age_list = []
        speed_list = []
        for i in final_nested_list:
            for j in range(len(i)):
                if j == 0:
                    speed_list.append(i[j])
                if j == 1:
                    age_list.append(i[j])
        speed_list.append(test_vector[0])
        age_list.append(test_vector[1])
        sorted_age_list = sorted(age_list)
        sorted_speed_list = sorted(speed_list)
        updated_age_speed = []
        for i in final_nested_list:
            person_results = []
            for j in range(len(i)):
                if j == 0:
                    normalized_speed = (i[j] - float(sorted_speed_list[0])) / (float(sorted_speed_list[-1]) - float(sorted_speed_list[0]))
                    person_results.append(normalized_speed)
                if j == 1:
                    normalized_age = (i[j] - int(sorted_age_list[0])) / (int(sorted_age_list[-1]) - int(sorted_age_list[0]))
                    person_results.append(normalized_age)
                elif j != 0 and j != 1:
                    person_results.append(i[j])
            updated_age_speed.append(person_results)
        return updated_age_speed, sorted_age_list, sorted_speed_list


    def euclidean_distance(a, b):
        distance = 0
        for a1, b1 in zip(a, b):
            distance += (a1 - b1) ** 2
        return math.sqrt(distance)


    def calc_dists(one_point, list_of_points):
        list_of_distances = []
        for point in list_of_points:
            list_of_distances.append(euclidean_distance(point, one_point))
        return list_of_distances


    def transform_test_case(test_list, age_list, speed_list, vector_dictionary):
        transformed_list = []
        for i in range(len(test_list)):
            if i == 0:
                normalized_speed = ((test_list[i] - speed_list[0]) / (speed_list[-1] - speed_list[0]))
                transformed_list.append(normalized_speed)
            elif i == 1:
                normalized_age = ((test_list[i] - age_list[0]) / (age_list[-1] - age_list[0]))
                transformed_list.append(normalized_age)
            elif i == len(test_list) - 1:
                vector_list = vector_dictionary.get(test_list[i])
                for b in vector_list:
                    transformed_list.append(b)
            elif (i != 0) and (i != 1) and (i != len(test_list) - 1):
                transformed_list.append(test_list[i])
        return transformed_list


    def k_closest_labels(test_vector, list_with_labels, k):
        data = []
        for i in range(len(test_vector)):
            label = 0
            if list_with_labels[i][0] == 'Yes':
                label = 1
            elif list_with_labels[i][0] == 'No':
                label = 0
            lable_n_distance = (test_vector[i], label)
            data.append(lable_n_distance)
        data.sort(key=lambda tup: tup[0])
        k_list_of_labels = []
        for i in range(k):
            k_list_of_labels.append(data[i][1])
        return k_list_of_labels


    def predict(test_vector, k):
        age_n_speed_list = normalize_age_speed_list(combined_list, test_vector)
        normalized_age_and_speed_list = age_n_speed_list[0]
        sorted_age_list = age_n_speed_list[1]
        sorted_speed_list = age_n_speed_list[2]
        transformed_test_vector = transform_test_case(test_vector, sorted_age_list, sorted_speed_list,
                                                          vector_dictionary)
        result = calc_dists(transformed_test_vector, normalized_age_and_speed_list)
        labes_and_distances_list = k_closest_labels(result, nested_list_without_spaces, k)
        return labes_and_distances_list


    def predict_result(k):
        test_vector_one = [424, 40, 1.42, 'nothing']
        test_vector_two = [210, 39, 3.19, 'cycling 3h']
        test_vector_three = [518, 33, 3.12, 'nothing']
        result_list = []
        for i in range(3):
            if i == 0:
                result_list.append(predict(test_vector_one, k))
            elif i == 1:
                result_list.append(predict(test_vector_two, k))
            elif i == 2:
                result_list.append(predict(test_vector_three, k))
        return result_list


    def form_print_statement(nested_list):
        response = []
        for i in nested_list:
            count_1 = 0
            count_0 = 0
            for j in i:
                if j == 0:
                    count_0 += 1
                elif j == 1:
                    count_1 += 1
            if count_0 > count_1:
                response.append(0)
            elif count_1 > count_0:
                response.append(1)
        return response


    nested_list_without_spaces = nested_list_nospaces()
    nested_list_converted = nested_list_converted_info(nested_list_without_spaces)
    converted_info = nested_list_converted[0]
    activity_list = nested_list_converted[1]
    vector_dictionary_n_raw_list = create_vectordict_prelist(activity_list)
    vector_dictionary = vector_dictionary_n_raw_list[0]
    vector_lists = vector_dictionary_n_raw_list[1]
    combined_list = create_combined_list(converted_info, vector_dictionary)

    for_k_one = predict_result(1)
    for_k_three = predict_result(3)
    for_k_five = predict_result(5)

    print('Result with k = 1:', form_print_statement(for_k_one))
    print('Result with k = 3:', form_print_statement(for_k_three))
    print('Result with k = 5:', form_print_statement(for_k_five))
