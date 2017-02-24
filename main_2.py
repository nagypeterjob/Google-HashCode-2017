import read_2
import difflib


def priority_videos(videos):
    for x in videos:
        x['priority'] = x['request_number'] * x['size']
        x['ideal'] = {}

    prio_videos = sorted(videos, key=lambda video: video[
                         'priority'], reverse=True)
    return prio_videos


def avg_cache_delay(endpoints, size):
    avg_delays = {}
    for x in endpoints:
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


def calculate_save(videos, endpoints, caches):
    video_saves = []
    i = 0
    len_vid = len(videos)
    for y in videos:
        saves = []
        i += 1
        if i % 100 == 0:
            print('calc_save ' + str(i) + '/' + str(len_vid))
            print()
        base_delay = calculate_base_delay(videos, y['id'], endpoints)
        for x in caches:
            save = base_delay - \
                calculate_cache_delay(videos, y['id'], endpoints, x['id'])
            if save > 0:
                saves.append([x['id'], save])
        saves.sort(key=lambda x: x[1], reverse=True)
        video_saves.append([y['id'], saves])
    return video_saves


def calculate_cache_delay(videos, video_id, endpoints, cache_id):
    for x in videos:
        if x['id'] == video_id:
            all_delay = 0
            for y in x['requests']:
                ok_z = False
                for z in endpoints:
                    if not ok_z:
                        if y == z['id']:
                            ok_z = True
                            cached = False
                            for t in z['cache']:
                                if not cached:
                                    if t['id'] == cache_id:
                                        cached = True
                                        all_delay += t['latency']
                            if not cached:
                                all_delay += z['d_latency']
            return all_delay


def calculate_base_delay(videos, video_id, endpoints):
    for x in videos:
        if x['id'] == video_id:
            all_delay = 0
            for y in x['requests']:
                ok_z = False
                for z in endpoints:
                    if not ok_z:
                        if y == z['id']:
                            ok_z = True
                            all_delay += z['d_latency']
            return all_delay


def optimize(saves, caches, videos):
    result = []
    for x in saves:
        ok = False
        video_size = 0

        for t in videos:
            if t['id'] == x[0]:
                video_size = t['size']

        for y in x[1]:
            if not ok:
                for z in caches:
                    if not ok:
                        if z['id'] == y[0]:
                            if z['rem_size'] >= video_size:
                                ok = True
                                z['rem_size'] -= video_size
                                if y[0] not in [x[0] for x in result]:
                                    result.append([y[0], [x[0]]])
                                else:
                                    for t in result:
                                        if y[0] == t[0]:
                                            t[1].append(x[0])
    result.sort(key=lambda x: x[0])
    return result


[input_array, videos, endpoints] = read_2.readFile('kittens.in')

videos = priority_videos(videos)

caches = avg_cache_delay(endpoints, input_array[4])

# for x in videos:
#     print(x)
# print()
# for x in caches:
#     print(x)
# print()
# for x in endpoints:
#     print(x)

saves = calculate_save(videos, endpoints, caches)

result = optimize(saves, caches, videos)

# for x in result:
#     print(x)

read_2.writeFile(result)
