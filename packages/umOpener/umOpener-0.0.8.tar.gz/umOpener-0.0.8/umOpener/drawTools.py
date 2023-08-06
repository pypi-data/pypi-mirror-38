# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt


def line(dates, LSTPoints, obsPoints, siteCode, name):
    newLSTPoints = []
    newLSTx = []
    for index, LSTPoint in enumerate(LSTPoints):
        if (LSTPoint != 0):
            newLSTPoints.append(LSTPoint)
            newLSTx.append(index)
    print newLSTPoints
    print newLSTx
    x = range(0, len(dates))
    # 设置图片的大小
    fig = plt.figure(figsize=(50, 20), dpi=80)

    ax = fig.add_subplot(1, 1, 1)

    # 绘制图片
    ax.plot(x, obsPoints)
    ax.plot(newLSTx, newLSTPoints)
    #
    ax.plot(dates, obsPoints, 'go-', label=u'obs', color="b")
    ax.plot(newLSTx, newLSTPoints, 'go-', label=u'hdf', color="r")
    legend = ax.legend(loc='upper right', shadow=False)

    # 设置x州的刻度
    # 调整x轴的刻度
    # 取步长，数字和字符一一对应，数据的长度一样
    plt.xticks(list(x)[::1], dates[::1], rotation=45)

    # 设置添加描述信息
    plt.xlabel('TIME')
    plt.ylabel('TMP')
    plt.title("%s" % siteCode)

    # 展示图片
    plt.savefig("./result/%s_%s.png" % (name, siteCode))


def testDraw(data):
    fig = plt.figure(figsize=(50, 20), dpi=80)
    ax = fig.add_subplot(1, 1, 1)
    cs = ax.imshow(data, cmap="jet")
    plt.colorbar(cs)
    plt.show()
