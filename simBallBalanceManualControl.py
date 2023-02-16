import time
import cv2
import math

def main():
    width = 300 #ウィンドウの幅
    height = 200 #ウィンドウの高さ
    max_length = 100 #棒の長さの半分
    dt = 0.1 #時間刻み
    gravity = 9.80665 #重力加速度
    s = 0.0 #レールの角度
    r = 10.0 #ボールの半径
    v = 0.0 #ボールの速度
    x = max_length - 10 #ボールの初期位置(初期位置は右側に配置)

    #シミュレーション
    while True:
        #ボールの位置更新
        costheta = math.cos(s)
        sintheta = math.sin(s)
        v = v + (gravity * sintheta) * dt
        if (x < max_length) and (v < 0):
            v = 0.0
        if (x > max_length) and (v > 0):
            v = 0.0
        x = x + v * dt

        #描画設定
        img = cv2.imread('300x200.bmp', flags=cv2.IMREAD_GRAYSCALE)
        y = height / 2 + x * math.tan(s) - r / costheta
        x1 = width / 2 + max_length * costheta
        y1 = height / 2 + max_length * sintheta
        x2 = width / 2 - max_length * costheta
        y2 = height / 2 - max_length * sintheta
        cv2.rectangle(img, (int(width / 2 - 20), int(0)),
                (int(width / 2 + 20), int(height)), 198, -1)
        cv2.circle(img, (int(x + width / 2), int(y)), int(r), 127, -1)
        cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), 32, 4)
        cv2.imshow('Simulation', img)

        #キー入力処理
        ds = 0.0
        k = cv2.waitKey(10)
        if k == 27: #Esc key
            cv2.destroyAllWindows()
            t = -1
            break
        elif k == 97: #a key
            ds = 0.01 #左側を上げる
        elif k == 115: #s key
            ds = -0.01 #右側を上げる
        
        #アーム角度更新
        s = s + ds

if __name__ == '__main__':
    main()
