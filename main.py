import read
from collections import OrderedDict

def priority_videos(videos):
    for x in videos:
        x['priority'] = x['request_number'] * x['size']
        # print(x)
        # print(x['priority'])
    prio_videos = sorted(videos, key=lambda video: video['priority'], reverse = True)
    # print(prio_videos)
    return prio_videos


def avg_cache_delay(endpoints,size):
    avg_delays = {}
    for x in endpoints:
        for y in x['cache']:
            if y['id'] in avg_delays:
                avg_delays[y['id']]['num'] += 1
                avg_delays[y['id']]['total_delay'] += y['latency']
            else:
                avg_delays[y['id']] = { }
                avg_delays[y['id']]['id'] = y['id']
                avg_delays[y['id']]['num'] = 1
                avg_delays[y['id']]['total_delay'] = y['latency']
                avg_delays[y['id']]['rem_size'] = size
    for x in avg_delays:
        avg_delays[x]['avg_delay'] = avg_delays[x]['total_delay']/avg_delays[x]['num']

    prio_caches = sorted(avg_delays.items(), key=lambda x:x[1]['avg_delay'])
    for x in range(len(prio_caches)):
        prio_caches[x] = prio_caches[x][1]
    return prio_caches

def cache(videos, endpoints):
    None

    # videos = prio_videos(videos)



[input_array, videos, endpoints] = read.readFile('me_at_the_zoo.in')

videos = priority_videos(videos)
caches = avg_cache_delay(endpoints,input_array[4])


def optimize(videos, caches):
    None
