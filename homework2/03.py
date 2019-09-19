import turtle

t3 = turtle.Turtle()


def draw_triangle(level):
    # 문제의 조건에 맞게 triangle을 그리려다 보면 한변의 길이를 조정해줘야 해서 새로운 함수를 만들고 길이변수값을 넣어주었다.
    def draw_fractal(d, level):
        # 프랙탈 삼각형중 제일 작은 크기의 경우 : base
        if level == 1:
            # 채워진 삼각형 그리기
            t3.begin_fill()
            # 밑변, 우변, 좌변의 순으로 그리고 오른쪽 방향으로 본 채 마무리
            for i in range(3):
                t3.forward(d)
                t3.left(120)
            t3.end_fill()
        # leve1>1인 경우
        else:
            # 작은 삼각형(한레벨 아래의 좌하단 삼각형) 부터 그리기(좌하단 작은 삼각형으로 재귀적으로 내려감. level이 하나씩 내려가면 길이는 반이됨.)
            draw_fractal(d/2, level-1)
            # 한레벨 아래의 좌하단 삼각형을 그리면 우하단 삼각형을 그리기 위해 좌하단 삼각형의 변만큼 오른쪽으로 이동.
            t3.forward(d/2)
            # 한레벨 아래의 우하단 삼각형 그리기.
            draw_fractal(d/2, level-1)
            # 좌하단 삼각형을 그린 위치로 돌아옴.
            t3.backward(d/2)
            # 중앙 위에 있는 삼각형을 그리기 위해 방향을 잡고 한레벨 아래의 삼각형의 변의 길이만큼 이동.
            t3.left(60)
            t3.forward(d/2)
            # 중앙 위 삼각형을 그리기 위해 우측으로 방향.
            t3.right(60)
            # 한레벨 아래의 중앙 위 삼각형 그리기
            draw_fractal(d/2, level-1)
            # 한레벨 아래의 좌하단 삼각형을 그린 위치로 돌아오고 방향은 오른쪽을 바라보게 함.
            t3.right(120)
            t3.forward(d/2)
            t3.left(120)

    # 도형 크기
    d = 300
    # 길이 변수 포함한 프랙탈 삼각형 그리기
    draw_fractal(d, level)


# 함수호출
draw_triangle(level=5)
# 일시정지
turtle.done()
