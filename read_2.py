import numpy as np


def readFile(filename):
    file = open(filename, "r")
    first_line = file.readline()
    first_line = first_line.split(' ')
    [video_num, endpoints_num, requests, caches, cache_size] = first_line

    video_num = int(video_num)
    endpoints_num = int(endpoints_num)
    requests = int(requests)
    caches = int(caches)
    cache_size = int(cache_size)

    videos = []
    endpoints = []

    second_line = file.readline()
    second_line = second_line.split(' ')

    i = 0
    for obj in second_line:
        videos.append({'id': i, 'size': int(obj),
                       'request_number': 0, 'requests': []})
        i += 1

    rows = file.readlines()
    file.close()

    index = 0
    for a in range(endpoints_num):
        data = rows[index].rstrip().split(' ')
        num_of_caches = int(data[1])
        endpoints.append({'id': a, 'd_latency': int(data[0])})
        index += 1
        if num_of_caches != 0:
            endpoints[a]['cache'] = []
            for b in range(num_of_caches):
                data = rows[index].rstrip().split(' ')
                id = int(data[0])
                latency = int(data[1])
                if latency < endpoints[a]['d_latency']:
                    endpoints[a]['cache'].append(
                        {'id': id, 'latency': latency})
                index += 1
    while(index < len(rows) - 1):
        index += 1
        data = rows[index].rstrip().split(' ')
        video_id = int(data[0])
        endpoint_id = int(data[1])
        req = int(data[2])
        videos[video_id]['request_number'] += req
        if endpoint_id not in videos[video_id]['requests']:
            videos[video_id]['requests'].append(endpoint_id)

    tmp = []

    for video in range(len(videos)):
        if len(videos[video]['requests']) != 0 and videos[video]['size'] <= cache_size:
            tmp.append(videos[video])
    videos = tmp
    tmp = []
    for endpoint in range(len(endpoints)):
        if 'cache' in endpoints[endpoint]:
            tmp.append(endpoints[endpoint])
    endpoints = tmp
    return [video_num, endpoints_num, requests, caches, cache_size], videos, endpoints


def writeFile(data):
    file = open('result_2.txt', 'w')
    file.write(str(len(data)) + '\n')
    for x in data:
        file.write(str(x[0]))
        file.write(' ')
        for y in x[1]:
            file.write(str(y))
            file.write(' ')
        file.write('\n')
    file.close()
