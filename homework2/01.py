import turtle

# turtle 객체 생성
t1 = turtle.Turtle()

# 선을 50개 그리기 위해 반복문 50번 반복
for i in range(50):
    # 50개의 선이 점점 증가하는 다른 길이를 가지도록 함
    t1.forward(i*10)
    # 하나의 선을 그린 후 반시계 방향 회전
    t1.left(90)

# 일시정지
turtle.done()
