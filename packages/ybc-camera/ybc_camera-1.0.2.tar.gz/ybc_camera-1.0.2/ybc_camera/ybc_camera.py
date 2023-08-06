import cv2
import time


def camera(filename=''):
    cap = cv2.VideoCapture(0)
    while 1:
        ret, frame = cap.read()
        cv2.imshow("capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            now = time.localtime()
            if filename == '':
                filename = str(now.tm_hour) + str(now.tm_min) + str(now.tm_sec) + '.jpg'
            cv2.imwrite(filename, frame)
            break
    cap.release()
    cv2.destroyAllWindows()
    return filename


def main():
    res = camera()
    print(res)


if __name__ == '__main__':
    main()
