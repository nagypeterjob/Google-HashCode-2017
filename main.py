import read
from collections import OrderedDict
import difflib


def priority_videos(videos):
    for x in videos:
        x['priority'] = x['request_number'] * x['size']
        x['ideal'] = {}
        # print(x)
        # print(x['priority'])
    prio_videos = sorted(videos, key=lambda video: video[
                         'priority'], reverse=True)
    # print(prio_videos)
    return prio_videos


def avg_cache_delay(endpoints, size):
    avg_delays = {}
    for x in endpoints:
        #     print(x)
        for y in x['cache']:
            if y['id'] in avg_delays:
                avg_delays[y['id']]['num'] += 1
                avg_delays[y['id']]['total_delay'] += y['latency']
                avg_delays[y['id']]['users'].append(x['id'])
            else:
                avg_delays[y['id']] = {}
                avg_delays[y['id']]['id'] = y['id']
                avg_delays[y['id']]['num'] = 1
                avg_delays[y['id']]['total_delay'] = y['latency']
                avg_delays[y['id']]['rem_size'] = size
                avg_delays[y['id']]['users'] = [x['id']]
    for x in avg_delays:
        avg_delays[x]['avg_delay'] = avg_delays[x][
            'total_delay'] / avg_delays[x]['num']

    prio_caches = sorted(avg_delays.items(), key=lambda x: x[1]['avg_delay'])
    for x in range(len(prio_caches)):
        prio_caches[x] = prio_caches[x][1]
    return prio_caches


def optimize(videos, caches2):
    tmp = {}
    for x in videos:
        best = 0
        best_1 = 0
        best_val = 10000000
        for z in x['ideal']:
            if x['ideal'][z] < best_val:
                best_1 = best
                best = z
        # print(x['ideal'][best])
        y = caches2[best]
        # print(y)
        if y['rem_size'] >= x['size']:
            # print(y['id'])
            if y['id'] in tmp:
                tmp[y['id']].append(x['id'])
            else:
                tmp[y['id']] = [x['id']]
            y['rem_size'] -= x['size']
        else:
            y = caches2[best_1]
            if y['rem_size'] >= x['size']:
                # print(y['id'])
                if y['id'] in tmp:
                    tmp[y['id']].append(x['id'])
                else:
                    tmp[y['id']] = [x['id']]
                y['rem_size'] -= x['size']
    return tmp


def optimize2(videos, caches):
    for x in videos:
        # print(x['id'])
        for y in caches:
            tmp = difflib.SequenceMatcher(
                None, x['requests'], y['users']).ratio()
            if tmp == 0:
                # print(x['ideal'])
                x['ideal'][y['id']] = 10000000
            else:
                x['ideal'][y['id']] = y['avg_delay'] / \
                    min(1, (difflib.SequenceMatcher(
                        None, x['requests'], y['users']).ratio() * 2))

        # print(x)
        # print()
    return videos


[input_array, videos, endpoints] = read.readFile('videos_worth_spreading.in')

videos = priority_videos(videos)
caches2 = avg_cache_delay(endpoints, input_array[4])

videos = optimize2(videos, caches2)

# for x in videos:
#     print(x['ideal'])
result = optimize(videos, caches2)
# for x in result:
#     print(x, result[x])
read.writeFile(result)
