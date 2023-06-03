import pickle
import sys

#将数据信息处理成可用的轨迹信息，并保存二进制文件

mouse_check_path=sys.path[0]+'\data\D=2000_W=100_mouse_check.bin'
mouse_move_path=sys.path[0]+'\data\D=2000_W=100_mouse_move.bin'
information_path=sys.path[0]+'\data\D=2000_W=100_information.bin'
track_path=sys.path[0]+'\data\D=2000_W=100_track.bin'

def save_track(mouse_check_path,mouse_move_path,track_path):
    '''
    模拟轨迹
    mouse_check_path:鼠标点击的位置和时间的二进制文件
    mouse_move_path:鼠标移动的位置和时间的二进制文件
    track_path:鼠标轨迹的二进制文件
    鼠标点击和移动是列表，(t,(x,y))
    
    鼠标轨迹，是一个列表，包含每一段轨迹的列表，每一段列表由一个元组组成，
    元组的第一个元素是记录时间，第二个元素是鼠标的x坐标，第三个元素是鼠标的y坐标(t,(x,y))
    '''
    divide_index=[]#记录鼠标移动和鼠标点击的分界点
    with open(mouse_check_path,'rb') as file:
        mouse_check=pickle.load(file)
    with open(mouse_move_path,'rb') as file:
        mouse_move=pickle.load(file)
    
    print('点击点的个数为：',len(mouse_check))
    for i in range(len(mouse_check)):
        for j in range(len(mouse_move)):
            if mouse_check[i][0]<mouse_move[j][0]:
                divide_index.append(j)
                break
    #得到切片的索引
    track=[]
    for i in range(0,len(divide_index)-1,2):
        track.append(mouse_move[divide_index[i]:divide_index[i+1]])
    
    print('总的轨迹长度为：',len(mouse_move))
    
    for i in range(len(track)):
        print(len(track[i]))
    with open(track_path, "wb") as file:
        pickle.dump(track, file)
    #print(track)
    print('轨迹保存成功')

save_track(mouse_check_path,mouse_move_path,track_path)