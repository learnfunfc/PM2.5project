import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import time
import csv



connect = serial.Serial("com15",9600,timeout=0.5) # set serail port
plt.rcParams['toolbar'] = 'None' #將工具列移除 必須放在 figure物件還沒產生前
fig,axes = plt.subplots(1,1,figsize=(7,6)) # to creat asxes object
fig.subplots_adjust(bottom=0.24)
timePoint = []
ysA=[]
t = 0 # 初始化紀錄次數
duration = 3000 # read data by how many milliseconds


# send '2' command to turn on fan
def send_on(event):
        connect.write(b"2")
# send '3' command to turn off fan
def send_off(event):
        connect.write(b'3')

# anima is used to difine how to show dynamic figure
def anima(i):
        
        global ysA
        global timePoint
        global t
        connect.write(b"1") # send '1' command for senor reading
        data = connect.readline() # read data from Ardunio
        data = data.decode("utf-8")
        data = data.rstrip("\r\n")

        if len(data)>3:
                t = t + 1
                data = data.rstrip("\r\n")
                data_list = data.split()
                
                ysA.append(float(data_list[0]))
                timePoint.append(t)
                date_t = time.strftime("%m/%d")
                date_hr = time.strftime("%H:%M:%S")
                record = "{} {} {} {}".format(date_t,date_hr,t,float(data_list[0]))
                print(record)
                record = [date_t,date_hr,t,float(data_list[0])]
                with open("sample.csv","a",newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(record)
                if len(ysA) > 100:
                        ysA = ysA[101:]
                        timePoint = timePoint[101:]
                              
        
        
        axes.clear()
        axes.set(title='PM2.5 Conc.') # 設子圖title
        axes.set_ylim(0,3500) #設定y軸範圍
        axes.grid(True)
        
        axes.plot(timePoint,ysA, label="PM2.5 value")
        axes.legend()
        



ani = animation.FuncAnimation(fig,anima, interval = duration)


rax1 = plt.axes([0.75, 0.02, 0.13, 0.15], frameon=True) #[水平 垂直 寬 高] [往右 往上] frameon 顯示
rax2 = plt.axes([0.55, 0.02, 0.13, 0.15], frameon=True)
button_on = plt.Button(rax1,"ON")
button_off = plt.Button(rax2,"OFF")

button_on.on_clicked(send_on)
button_off.on_clicked(send_off)
plt.show()



    
    
