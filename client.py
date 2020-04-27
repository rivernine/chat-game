import socket 
from _thread import *
import threading 
import time
import signal
import sys

host = '52.79.240.77'
main_port = 12341
notice_port = main_port + 10
main_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
notice_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

def interrupt_handler(signum, f):
    main_sock.send('/exit'.encode())
    print("Bye~")
    sys.exit()

def notice_thread():
    while True:
        print(notice_sock.recv(1024).decode())

def compare(str1, str2):
    ret = 0
    strLong, strShort = str1, str2
    if len(str1) < len(str2):
        strLong, strShort = str2, str1

    for i in range(0, len(strShort) - 1):
        if str1[i] == str2[i]:
            ret = ret + 1
    return ret 

def Main():
    main_sock.connect((host, main_port)) 
    notice_sock.connect((host, notice_port)) 
    # 로그인
    print(main_sock.recv(1024).decode())
    id = input()
    main_sock.send(id.encode())
    # Notice Socket
    start_new_thread(notice_thread, ())
    while True: 
        print('[ Menu ]')
        print('\'/start [num]\' : Start')
        print('\'/rank\'        : Show rank')
        print('\'/exit\'        : Exit')
        menu = input()        
        main_sock.send(menu.encode())
        if menu[:6] == '/start' and len(menu) > 6:
            count = int(menu[7:])
            for i in range(0, count):
                question = main_sock.recv(1024)
                print(question.decode())
                # 시간 측정
                start = time.time()
                my = input()
                record = time.time() - start
                record = int( len(question.decode()) * 60 / record )
                # 정확도 측정
                accuracy = 100 
                if question.decode() != my:
                    accuracy = int( compare(question.decode(), my) / len(question.decode()) * 100 )
                # 출력
                print('[ %s / %s%% ]' %(str(record), str(accuracy)))
                if my == '':
                    main_sock.send(" ".encode())
                else:
                    main_sock.send(my.encode())
        elif menu == '/rank':
            print(main_sock.recv(1024).decode())
        elif menu == '/exit':
            break
        else:
            print("Error")
    notice_sock.close() 
    main_sock.close() 

if __name__ == '__main__': 
    signal.signal(signal.SIGINT, interrupt_handler)
    Main() 
