import cv2
import sys

cap = cv2.VideoCapture(0)

# 열렸는지 확인
if not cap.isOpened():
    print("Camera open failed!")
    sys.exit()

# 웹캠의 속성 값을 받아오기
# 정수 형태로 변환하기 위해 round
w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS) # 카메라에 따라 값이 정상적, 비정상적

# fourcc 값 받아오기, *는 문자를 풀어쓰는 방식, *'DIVX' == 'D', 'I', 'V', 'X'
fourcc = cv2.VideoWriter_fourcc(*'DIVX')

# 1프레임과 다음 프레임 사이의 간격 설정
delay = round(1000/fps)

# 웹캠으로 찰영한 영상을 저장하기
# cv2.VideoWriter 객체 생성, 기존에 받아온 속성값 입력
out = cv2.VideoWriter('output.avi', fourcc, fps, (w, h))

# 제대로 열렸는지 확인
if not out.isOpened():
    print('File open failed!')
    cap.release()
    sys.exit()

# 프레임을 받아와서 저장하기
while True:                 # 무한 루프
    ret, frame = cap.read() # 카메라의 ret, frame 값 받아오기

    if not ret:             #ret이 False면 중지
        break

    inversed = ~frame # 반전

    edge = cv2.Canny(frame, 50, 150) # 윤곽선

    # 윤곽선은 그레이스케일 영상이므로 저장이 안된다. 컬러 영상으로 변경
    edge_color = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)

    out.write(edge_color) # 영상 데이터만 저장. 소리는 X

    cv2.imshow('frame', frame)
    cv2.imshow('inversed', inversed)
    cv2.imshow('edge', edge)

    if cv2.waitKey(delay) == 27: # esc를 누르면 강제 종료
        break

cap.release()
out.release()
cv2.destroyAllWindows()