import time, win32con, win32api, win32gui, ctypes

# 채팅방 이름
kakaoRoomName = ["고1 쌤없 반톡"]

_user32 = ctypes.WinDLL("user32")
PostMessage = win32api.PostMessage
SendMessage = win32gui.SendMessage
FindWindow = win32gui.FindWindow

def getTime(type):
    return {
        "요일": time.strftime("%a", time.localtime(time.time())),
        "시": int(time.strftime("%H", time.localtime(time.time()))),
        "분": int(time.strftime("%M", time.localtime(time.time()))),
        "초": int(time.strftime("%S", time.localtime(time.time())))
    }.get(type, "DEFAULT")

def kakaoSendText(roomName, text):
    hwnd = win32gui.FindWindowEx(win32gui.FindWindow(None, roomName), None, "RichEdit50W", None)
    win32api.SendMessage(hwnd, win32con.WM_SETTEXT, 0, text)
    SendReturn(hwnd)

def SendReturn(hwnd):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    time.sleep(0.1)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

while True:
    cnt = 0
    day, hour, minute, second = getTime("요일"), getTime("시"), getTime("분"), getTime("초")
    ok_day = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    start_hour = 9
    term_hour = 1
    end_hour = 15 if day == "Wed" else 16 # 수요일은 15시까지, 다른 날은 16시까지
    ok_hour = [i for i in range(start_hour, end_hour+1, term_hour)] # 1시간마다 전송
    send_min = 50 if hour < 13 else 40 # 점심 전까지는 50분에, 이후에는 40분에 안내
    message = "📢 [Bot] 현재 시간 {0}시 {1}분을 지나가고 있습니다.\n" \
              "1학년 5반 학생들은 금일 {2}시 40분까지 [베네듀 일일 과제]를 신속히 완료하시기 바랍니다.".format(hour, minute, end_hour)

    for room in kakaoRoomName:
        if(day in ok_day):
            if(hour in ok_hour and minute == send_min):
                cnt = 0
                kakaoSendText(room, message)
                time.sleep(0.5)
                print(f'{hour}시 {minute}분 {second}초, "{room}"방에 [{message}]를 전송했습니다\n')
                time.sleep(0.5)
            else:
                if(not(cnt)):
                    print(f'{send_min}분이 되면 전송합니다')
                    cnt += 1
                time.sleep(1)
        else:
            print("전송 가능한 시간이 아닙니다. 프로그램을 종료합니다", end="")
            exit()

    time.sleep(60)
