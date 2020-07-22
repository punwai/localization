import pandas as pd

df = pd.read_csv("./Data/Pun-5_51907a2f2e7fb94d_label.csv")
print(df.head(5))

max_labels = max(df["label"])
l_index = 0

transition_times = []
transition_counts = []

print(max_labels)

for i in range(max_labels):
    max_time = df.loc[df.loc[df.label == i]["routerTime"].idxmax(), "routerTime"]
    min_time = df.loc[df.loc[df.label == (i+1)]["routerTime"].idxmin(), "routerTime"]
    max_count = df.loc[df.loc[df.label == i]["routerTime"].idxmax(), "count"]
    min_count = df.loc[df.loc[df.label == (i+1)]["routerTime"].idxmin(), "count"]

    print(max_time, min_time)
    transition_times.append(int((max_time + min_time) / 2))
    transition_counts.append((int((max_count + min_count) / 2))%256)

print(transition_times)
print(transition_counts)

count_number = 3
count_channel = 4
transition_filter = 10000

transition_snapshots = []

def produce_count_range(first, last):
    count_range = []
    last += 256
    difference = ((last-first)%256 )+1
    for i in range(difference):
        count_range.append((first+i)%256)
    return count_range

for i in range(len(transition_times)):
    transition_snapshot_front = []
    transition_snapshot_back = []
    t_time = transition_counts[i]
    t_count = transition_counts[i]
    for j in range(count_number):
        window_start = j * count_channel
        
        #furthest from transition state
        min_back = ((t_count + 256) - window_start - count_channel) % 256
        #closest to transition state
        max_back = ((t_count + 256) - window_start - 1) % 256

        back_range = produce_count_range(min_back,max_back)
        back_snapshot = df.loc[(df.label == i) & (df['count'].isin(back_range))]
        back_snapshot_json = {}

        #furthest from transition state
        max_front = ((t_count) + window_start + count_channel - 1) % 256
        #closest to transition state
        min_front = ((t_count) + window_start) % 256

        front_range = produce_count_range(min_front,max_front)
        front_snapshot = df.loc[(df.label == i+1) & (df['count'].isin(front_range))]
        front_snapshot_json = {}

        routerSerials = front_snapshot.routerSerial.unique()

        for rs in routerSerials:
            mean = front_snapshot.loc[front_snapshot.routerSerial == rs]['ri'].mean()
            front_snapshot_json[rs] = mean

        routerSerials = back_snapshot.routerSerial.unique()

        for rs in routerSerials:
            mean = back_snapshot.loc[back_snapshot.routerSerial == rs]['ri'].mean()
            back_snapshot_json[rs] = mean
            
        transition_snapshot_front.append(front_snapshot_json)
        transition_snapshot_back.append(back_snapshot_json)

    transition_snapshots.append(
        {
            "front": transition_snapshot_front,
            "back": transition_snapshot_back
        }
    )

    if(i == 1):
        break
    transition_times[i]
    transition_counts[i]

print(transition_snapshots)
