import cv2
 
vc = cv2.VideoCapture("D:\School\Opencv/1.mp4")  # 读入视频文件
# vc = cv2.VideoCapture("C:/Users/jason/Desktop/152821AA.MP4")
 
rval, firstFrame = vc.read()
firstFrame = cv2.resize(firstFrame, (640, 360), interpolation=cv2.INTER_CUBIC)
gray_firstFrame = cv2.cvtColor(firstFrame, cv2.COLOR_BGR2GRAY)   # 灰度化
firstFrame = cv2.GaussianBlur(gray_firstFrame, (21, 21), 0)      #高斯模糊，用于去噪
prveFrame = firstFrame.copy()
 
 
#遍历视频的每一帧
cars=[]
th=900;
count=0;
while True:
    (ret, frame) = vc.read()
    (ret, frame) = vc.read()
    (ret, frame) = vc.read()

    # 如果没有获取到数据，则结束循环
    if not ret:
        break
 
    # 对获取到的数据进行预处理
    frame = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_CUBIC)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (1, 1), 0)
    cv2.imshow("Current Frame", gray_frame)
    cv2.imshow("Prvevious Frame", prveFrame)
 
    # 计算当前帧与上一帧的差别
    frameDiff = cv2.absdiff(prveFrame, gray_frame)
    cv2.imshow("Frame Difference", frameDiff)
    prveFrame = gray_frame.copy()
 
 
    # 忽略较小的差别
    retVal, thresh = cv2.threshold(frameDiff, 20, 255, cv2.THRESH_BINARY)
  
 
    # 对阈值图像进行填充补洞
    thresh = cv2.dilate(thresh, None, iterations=2  )
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
   # text = "Unoccupied"
    # 遍历轮廓
    cv2.line(frame,(100,0),(100,360),(0,0,255),3)
    cv2.putText(frame,"Count:"+str(count),(360,130),0,1,(255,0,0),2)
    
    for contour in contours:
        # if contour is too small, just ignore it
        if cv2.contourArea(contour) < 750:   #面积阈值
            continue

        # 计算最小外接矩形（非旋转）
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.rectangle(thresh, (x, y), (x + w, y + h), (255, 255, 255), 2)
        #text = "Occupied!"
        non_exist=True
        center=[x+w/2,y+h/2]
        for i in range(len(cars)-1):
            if((cars[i][0]-center[0])**2+(cars[i][1]-center[1])**2<th):
                cars[i]=center
                non_exist=False
                break
        if center[0]>100:
            non_exist=False
        
        if (non_exist):
            cars.append(center)
            
    for i in range(len(cars)-1,-1,-1):
        if cars[i][0]>100:
            cars.remove(cars[i])
            count+=1
    cv2.putText(frame,"Valid:"+str(len(cars)),(360,160),0,1,(255,0,0),2)
    #cv2.putText(frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    #cv2.putText(frame, "F{}".format(frameCount), (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
 
    cv2.imshow('Result', frame)
    cv2.imshow('Binarization', thresh)
    cv2.imshow('Frame Difference', frameDiff)
 
    # 处理按键效果
    key = cv2.waitKey(60) & 0xff
    if key == 27:  # 按下ESC时，退出
        cv2.destroyAllWindows()
        break
    elif key == ord(' '):  # 按下空格键时，暂停
        cv2.waitKey(0)
 
    cv2.waitKey(0)
 
vc.release()