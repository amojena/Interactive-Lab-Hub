
import matplotlib.pyplot as plt
import numpy as np


def GetHistory():
    filename = "history.txt"
    history = []
    date= []
    avg_time= []
    impressions= []
    engagement= []

    with open(filename, "r") as f:
        lines = f.readlines()

    for line in lines:
        # print(filename)
        date1, avg_time1, impressions1, engagement1 = line.split(",")
        date.append(date1)
        avg_time.append(float(avg_time1))
        impressions.append(int(impressions1))
        engagement.append(int(engagement1.rstrip()))

    width = 0.35       # the width of the bars: can also be len(x) sequence

    fig, ax = plt.subplots()

    # ax.bar(date, engagement, width,  label='engagement')
    # ax.bar(date, impressions, width,  bottom=engagement,
    #        label='impressions')
    X = np.arange(7)
    ax.bar(X + 0.00, impressions, color = 'b', width = 0.25)
    ax.bar(X + 0.25, engagement, color = 'g', width = 0.25)

    ax.set_ylabel('impressions')
    ax.legend(labels=['impressions', 'engagement'])
    ax.set_xticks(X)
    ax.set_xticklabels(date)
    print(date)
    # ax.set_title('Scores by group and gender')
    # ax.legend()

    plt.savefig("graph.png")

if __name__ == '__main__':
	GetHistory()



