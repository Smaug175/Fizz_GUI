"""
(*)~----------------------------------------------------------------------------------
 Pupil Helpers
 Copyright (C) 2012-2016  Pupil Labs

 Distributed under the terms of the GNU Lesser General Public License (LGPL v3.0).
 License details are in the file license.txt, distributed as part of this software.
----------------------------------------------------------------------------------~(*)
"""

"""
This example demonstrates how to send simple messages to the Pupil Remote plugin
    'R' start recording with auto generated session name
    'R rec_name' start recording and name new session name: rec_name
    'r' stop recording
    'C' start currently selected calibration
    'c' stop currently selected calibration
    'T 1234.56' Timesync: make timestamps count form 1234.56 from now on.
    't' get pupil timestamp
    '{notification}' send a notification via pupil remote.
    本例演示了如何向 Pupil Remote 插件发送简单信息
    R "使用自动生成的会话名称开始录音
    R rec_name "开始录音并命名新会话名称：rec_name
    r'停止录音
    C'开始当前选择的校准
    c'停止当前选择的校准
    T 1234.56' 时间同步：从现在起，时间戳以 1234.56 的形式计数。
    t'获取瞳孔时间戳
    {notification}'通过瞳孔远程发送通知。
"""

import zmq
import msgpack as serializer
from time import sleep, time

if __name__ == "__main__":
    

    # Setup zmq context and remote helper
    ctx = zmq.Context()
    socket = zmq.Socket(ctx, zmq.REQ)
    socket.connect("tcp://127.0.0.1:50020")

    # Measure round trip delay
    t = time()
    socket.send_string("t")
    print(socket.recv_string())
    print("Round trip command delay:", time() - t)

    # set current Pupil time to 0.0
    socket.send_string("T 0.0")
    print(socket.recv_string())

    # start recording
    sleep(1)
    socket.send_string("R")
    print(socket.recv_string())

    sleep(5)
    socket.send_string("r")
    print(socket.recv_string())

    '''# send notification:
    def notify(notification):
        """Sends ``notification`` to Pupil Remote"""
        topic = "notify." + notification["subject"]
        payload = serializer.dumps(notification, use_bin_type=True)
        socket.send_string(topic, flags=zmq.SNDMORE)
        socket.send(payload)
        return socket.recv_string()

    # test notification, note that you need to listen on the IPC to receive notifications!
    # 请注意，您需要监听 IPC 才能接收通知！
    notify({"subject": "calibration.should_start"})
    sleep(5)
    notify({"subject": "calibration.should_stop"})'''
