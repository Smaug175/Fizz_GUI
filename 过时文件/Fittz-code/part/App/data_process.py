
'''
biao_qian = {
            'x':x,
            'y':SCREEN_HEIGHT-y,
            'time':datetime.datetime.now()
        }
'''
import datetime


def process_data(mouse_list,niukou_size):
    long = len(mouse_list)
    #开始时间
    string0 = str(mouse_list[0]['time'])
    min0 = int(string0[14:16])
    sec0 = float(string0[17:])
    tim0 = min0 * 60 + sec0
    #最终时间
    string = str(mouse_list[long-1]['time'])
    min = int(string[14:16])
    sec = float(string[17:])
    tim = min * 60 + sec
    #总时间
    Tim = tim - tim0

    #总距离
    Direct = ((mouse_list[0]['x']-mouse_list[long-1]['x'])**2 + (mouse_list[0]['y']-mouse_list[long-1]['y'])**2)**0.5


    return (Tim,Direct,niukou_size)


import numpy as np
def write_data(worksheet,T_H_R):
    r_a=[]
    r_b=[]
    for i in range(len(T_H_R)):
        worksheet.write(i+1, 0, label=T_H_R[i][0])
        worksheet.write(i+1, 1, label=T_H_R[i][1])
        worksheet.write(i+1, 2, label=T_H_R[i][2])
        log2 = np.log2(T_H_R[i][1]/T_H_R[i][2])
        worksheet.write(i + 1, 3, label=log2)

    for i in range(len(T_H_R)):
        for j in range(i, len(T_H_R), 1):
            if i !=j :
                t0 = T_H_R[i][0]
                w0 = np.log2(T_H_R[i][1]/T_H_R[i][2])
                t1 = T_H_R[j][0]
                w1 = np.log2(T_H_R[j][1]/T_H_R[j][2])
                a = (t0-t1)/(w0-w1)
                b = (w0*t1-w1*t0)/(w0-w1)
                r_a.append(a)
                r_b.append(b)

    for i in range(len(r_a)):
        worksheet.write(i+1, 4, label=r_a[i])
        worksheet.write(i+1, 5, label=r_b[i])

    return r_a,r_b




