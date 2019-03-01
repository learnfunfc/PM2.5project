import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import time
import csv
#setup serial port 
port = "COM7"
#port = "/dev/cu.usbmodem1421"

connect = serial.Serial(port,9600,timeout=0.5) # serail port connection
# create tk gui 
root = tkinter.Tk()
root.wm_title("PM2.5感測器數值")
root.geometry("700x600")

# create figure by pyplot module
fig,axes = plt.subplots(1,1,figsize=(7,5)) # to creat asxes object
fig.subplots_adjust(bottom=0.24)

''' set global variables '''
timePoint = []
ysA=[]
t = 0 # 初始化紀錄次數
duration = 3000 # read data by how many milliseconds
PM2_5_value="0.0"

'''define functions for each button  '''
# send '2' command to turn on fan
def send_on():
        connect.write(b"2")
# send '3' command to turn off fan
def send_off():
        connect.write(b'3')

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

def show_pm():
    global PM2_5_value
    left['text']=PM2_5_value
    root.after(duration,show_pm)

def anima(i):
        
        global ysA
        global timePoint
        global t
        global PM2_5_value
        
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
                PM2_5_value = data_list[0] # get PM2.5 value to show in labelFrame
                record = "{} {} {} {}".format(date_t,date_hr,t,float(data_list[0]))
                print(record)

                # write data into csv file 
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
        axes.plot([1,2,3,4,5],ysA, label="PM2.5 value")
        axes.plot(timePoint,ysA, label="PM2.5 value")
        axes.legend()

        
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw() # 內部是一個迴圈
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

# 執行pyplot figure update
ani = animation.FuncAnimation(fig,anima, interval = duration) 

'''定義每一個按鈕'''
button1 = tkinter.Button(master=root, text="Start",height = 3,width=5, pady=3, command=send_on,relief=tkinter.RAISED)
button1.place(relx = 0.9,rely=0.85)
button2 = tkinter.Button(master=root, text="Stop",height = 3,width=5, pady=3, relief=tkinter.RAISED,command=send_off)
button2.place(relx = 0.8,rely=0.85)
button3 = tkinter.Button(master=root, text="Quit",height = 3, width=5,pady=3,command = quit)
button3.place(relx = 0.7,rely=0.85)


'''define label frame to show PM2.5 value '''
labelframe = tkinter.LabelFrame(root, text = "PM2.5 value",height =20,width=20)
labelframe.pack(side=tkinter.LEFT, expand =0)
left = tkinter.Label(labelframe, text =PM2_5_value ,height =20,width=20)
left.pack(side=tkinter.LEFT)
root.after(duration,show_pm)




tkinter.mainloop()
