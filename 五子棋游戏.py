import tkinter as tk
import sys
import random
import pygame
from pygame.locals import *
import pygame.gfxdraw
from checkerboard import Checkerboard, BLACK_CHESSMAN, WHITE_CHESSMAN, offset, Point

a=input("""人人对战对应1；人机对战对应2，
           请选择：""")
if a=='1':

    PIECE_SIZE = 10
    click_x = 0
    click_y = 0

    a = 0
    b = 0

    pieces_x = [i for i in range(32, 523, 35)]
    pieces_y = [i for i in range(38, 529, 35)]

    coor_black = []
    coor_white = []

    person_flag = 1
    piece_color = "black"


    def showChange(color):
        global piece_color
        piece_color = color
        side_canvas.delete("show_piece")
        side_canvas.create_oval(110 - PIECE_SIZE, 25 - PIECE_SIZE,
                                110 + PIECE_SIZE, 25 + PIECE_SIZE,
                                fill=piece_color, tags=("show_piece"))


    def pushMessage():
        if person_flag == -1:
            var1.set("白棋赢")
        elif person_flag == 1:
            var1.set("黑棋赢")
        var2.set("Game Over")

    def piecesCount(coor, pieces_count, t1, t2):
        for i in range(1, 5):
            (x, y) = (click_x + t1 * 35 * i, click_y + t2 * 35 * i)
            if (x, y) in coor:
                pieces_count += 1
            else:
                break
        return pieces_count


    def coorBack(event):
        global click_x, click_y
        click_x = event.x
        click_y = event.y
        coorJudge()


    def gameReset():
        global person_flag, coor_black, coor_white, piece_color
        person_flag = 1
        var.set("黑棋先下")
        var1.set("")
        var2.set("")
        showChange("black")
        canvas.delete("piece")
        coor_black = []
        coor_white = []

    def preJudge(piece_color):
        if piece_color == "black":
            realJudge0(coor_black)
        elif piece_color == "white":
            realJudge0(coor_white)


    def realJudge0(coor):
        global person_flag, person_label
        if realJudge1(coor) == 1 or realJudge2(coor) == 1:
            pushMessage()
            person_flag = 0


    def realJudge1(coor):
        pieces_count = 0
        pieces_count = piecesCount(coor, pieces_count, 1, 0)  # 右边
        pieces_count = piecesCount(coor, pieces_count, -1, 0)  # 左边
        if pieces_count >= 4:
            return 1
        else:
            pieces_count = 0
            pieces_count = piecesCount(coor, pieces_count, 0, -1)  # 上边
            pieces_count = piecesCount(coor, pieces_count, 0, 1)  # 下边
            if pieces_count >= 4:
                return 1
            else:
                return 0


    def realJudge2(coor):
        pieces_count = 0
        pieces_count = piecesCount(coor, pieces_count, 1, 1)  # 右下角
        pieces_count = piecesCount(coor, pieces_count, -1, -1)  # 左上角
        if pieces_count >= 4:
            return 1
        else:
            pieces_count = 0
            pieces_count = piecesCount(coor, pieces_count, 1, -1)  # 右上角
            pieces_count = piecesCount(coor, pieces_count, -1, 1)  # 左下角
            if pieces_count >= 4:
                return 1
            else:
                return 0

    def putPiece(piece_color):
        global coor_black, coor_white
        canvas.create_oval(click_x - PIECE_SIZE, click_y - PIECE_SIZE, click_x + PIECE_SIZE, click_y + PIECE_SIZE,
                           fill=piece_color, tags=("piece"))

        if piece_color == "white":
            coor_white.append((click_x, click_y))
        elif piece_color == "black":
            coor_black.append((click_x, click_y))
        preJudge(piece_color)

    def coorJudge():
        global click_x, click_y
        coor = coor_black + coor_white
        global person_flag, show_piece
        item = canvas.find_closest(click_x, click_y)
        tags_tuple = canvas.gettags(item)
        if len(tags_tuple) > 1:
            tags_list = list(tags_tuple)
            coor_list = tags_list[:2]
            try:
                for i in range(len(coor_list)):
                    coor_list[i] = int(coor_list[i])
            except ValueError:
                pass
            else:
                coor_tuple = tuple(coor_list)
                (click_x, click_y) = coor_tuple
                if ((click_x, click_y) not in coor) and (click_x in pieces_x) and (click_y in pieces_y):

                    if person_flag != 0:
                        if person_flag == 1:
                            putPiece("black")
                            showChange("white")
                            var.set("轮白棋")
                        elif person_flag == -1:
                            putPiece("white")
                            showChange("black")
                            var.set("轮黑棋")
                        person_flag *= -1

    root = tk.Tk()
    root.title("五子定乾坤-人人对战")
    root.geometry("760x560")

    side_canvas = tk.Canvas(root, width=220, height=50)
    side_canvas.grid(row=0, column=1)
    side_canvas.create_oval(110 - PIECE_SIZE, 25 - PIECE_SIZE, 110 + PIECE_SIZE, 25 + PIECE_SIZE, fill=piece_color,
                            tags=("show_piece"))

    var = tk.StringVar()
    var.set("黑棋先下")
    person_label = tk.Label(root, textvariable=var, width=12, anchor=tk.CENTER,
                            font=("Arial", 20))
    person_label.grid(row=1, column=1)

    var1 = tk.StringVar()
    var1.set("")
    result_label = tk.Label(root, textvariable=var1, width=12, height=4,

                            anchor=tk.CENTER, fg="red", font=("Arial", 25))

    result_label.grid(row=2, column=1, rowspan=2)

    var2 = tk.StringVar()
    var2.set("")
    game_label = tk.Label(root, textvariable=var2, width=12, height=4, anchor=tk.CENTER, font=("Arial", 18))
    game_label.grid(row=4, column=1)

    reset_button = tk.Button(root, text="Restart", font=20, width=8, command=gameReset)
    reset_button.grid(row=5, column=1)


    canvas = tk.Canvas(root, bg="peachpuff", width=540, height=540)
    canvas.bind("<Button-1>", coorBack)  # 鼠标单击事件绑定
    canvas.grid(row=0, column=0, rowspan=6)

    for i in range(15):
        canvas.create_line(32, (35 * i + 38), 522, (35 * i + 38))
        canvas.create_line((35 * i + 32), 38, (35 * i + 32), 528)

    point_x = [3, 3, 11, 11, 7]
    point_y = [3, 11, 3, 11, 7]
    for i in range(5):
        canvas.create_oval(35 * point_x[i] + 28, 35 * point_y[i] + 33, 35 * point_x[i] + 36, 35 * point_y[i] + 41,
                           fill="black")

    for i in pieces_x:
        for j in pieces_y:
            canvas.create_oval(i - PIECE_SIZE, j - PIECE_SIZE, i + PIECE_SIZE, j + PIECE_SIZE, width=0,
                               tags=(str(i), str(j)))

    for i in range(15):
        label = tk.Label(canvas, text=str(i + 1), fg="black", bg="mistyrose", width=2, anchor=tk.E)
        label.place(x=2, y=35 * i + 28)

    count = 0
    for i in range(15):
        label = tk.Label(canvas, text=str(i + 1), fg="black", bg="mistyrose", width=2, anchor=tk.E)
        label.place(x=35 * i + 28, y=2)

    root.mainloop()
elif a=='2':
    b=input("请选择机人子的颜色，1代表蓝色，2代表黑色")
    from collections import namedtuple
    SIZE = 30
    Line_Points = 19
    Outer_Width = 20
    Border_Width = 4
    Inside_Width = 4
    Border_Length = SIZE * (Line_Points - 1) + Inside_Width * 2 + Border_Width
    Start_X = Start_Y = Outer_Width + int(Border_Width / 2) + Inside_Width
    SCREEN_HEIGHT = SIZE * (Line_Points - 1) + Outer_Width * 2 + Border_Width + Inside_Width * 2
    SCREEN_WIDTH = SCREEN_HEIGHT + 200

    Stone_Radius = SIZE // 2 - 3
    Stone_Radius2 = SIZE // 2 + 3
    Checkerboard_Color = (0xE0, 0xE2, 0x45)  # 棋盘颜色
    BLACK_COLOR = (10, 10, 10)
    WHITE_COLOR = (245, 245, 245)
    RED_COLOR = (200, 30, 30)
    BLUE_COLOR = (30, 30, 200)

    RIGHT_INFO_POS_X = SCREEN_HEIGHT + Stone_Radius2 * 2 + 10
    Chessman = namedtuple('Chessman', 'Name Value Color')
    Point = namedtuple('Point', 'X Y')

    if b == '1':
      BLACK_CHESSMAN = Chessman('黑子', 1, (95, 75, 215))
    elif b == '2':
        BLACK_CHESSMAN = Chessman('黑子', 1, (15, 15, 15))
    WHITE_CHESSMAN = Chessman('白子', 2, (219, 219, 219))

    offset = [(1, 0), (0, 1), (1, 1), (1, -1)]


    class Checkerboard:
        def __init__(self, line_points):
            self._line_points = line_points
            self._checkerboard = [[0] * line_points for _ in range(line_points)]

        def _get_checkerboard(self):
            return self._checkerboard

        checkerboard = property(_get_checkerboard)


        def can_drop(self, point):
            return self._checkerboard[point.Y][point.X] == 0

        def drop(self, chessman, point):

            #print(f'{chessman.Name} ({point.X}, {point.Y})')
            print(f'({point.X}, {point.Y})'+'处下子')
            self._checkerboard[point.Y][point.X] = chessman.Value

            if self._win(point):
                print(f'{chessman.Name}胜利了')
                return chessman

        def _win(self, point):
            cur_value = self._checkerboard[point.Y][point.X]
            for os in offset:
                if self._get_count_on_direction(point, cur_value, os[0], os[1]):
                    return True

        def _get_count_on_direction(self, point, value, x_offset, y_offset):
            count = 1
            for step in range(1, 5):
                x = point.X + step * x_offset
                y = point.Y + step * y_offset
                if 0 <= x < self._line_points and 0 <= y < self._line_points and self._checkerboard[y][x] == value:
                    count += 1
                else:
                    break
            for step in range(1, 5):
                x = point.X - step * x_offset
                y = point.Y - step * y_offset
                if 0 <= x < self._line_points and 0 <= y < self._line_points and self._checkerboard[y][x] == value:
                    count += 1
                else:
                    break

            return count >= 5

    if b=='1' :
      def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
          imgText = font.render(text, True, fcolor)
          screen.blit(imgText, (x, y))
    elif b=='2':
        def print_text(screen, font, x, y, text, fcolor=(15 , 75, 95)):
            imgText = font.render(text, True, fcolor)
            screen.blit(imgText, (x, y))

    def main():
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('五子定乾坤-人机大战')

        font1 = pygame.font.SysFont('SimHei', 32)
        font2 = pygame.font.SysFont('SimHei', 72)
        fwidth, fheight = font2.size('黑方获胜')

        checkerboard = Checkerboard(Line_Points)
        cur_runner = BLACK_CHESSMAN
        winner = None
        computer = AI(Line_Points, WHITE_CHESSMAN)

        black_win_count = 0
        white_win_count = 0
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        if winner is not None:
                            winner = None
                            cur_runner = BLACK_CHESSMAN
                            checkerboard = Checkerboard(Line_Points)
                            computer = AI(Line_Points, WHITE_CHESSMAN)
                elif event.type == MOUSEBUTTONDOWN:
                    if winner is None:
                        pressed_array = pygame.mouse.get_pressed()
                        if pressed_array[0]:
                            mouse_pos = pygame.mouse.get_pos()
                            click_point = _get_clickpoint(mouse_pos)
                            if click_point is not None:
                                if checkerboard.can_drop(click_point):
                                    winner = checkerboard.drop(cur_runner, click_point)
                                    if winner is None:
                                        cur_runner = _get_next(cur_runner)
                                        computer.get_opponent_drop(click_point)
                                        AI_point = computer.AI_drop()
                                        winner = checkerboard.drop(cur_runner, AI_point)
                                        if winner is not None:
                                            white_win_count += 1
                                        cur_runner = _get_next(cur_runner)
                                    else:
                                        black_win_count += 1
                            else:
                                print('超出棋盘区域')

            _draw_checkerboard(screen)

            for i, row in enumerate(checkerboard.checkerboard):
                for j, cell in enumerate(row):
                    if cell == BLACK_CHESSMAN.Value:
                        _draw_chessman(screen, Point(j, i), BLACK_CHESSMAN.Color)
                    elif cell == WHITE_CHESSMAN.Value:
                        _draw_chessman(screen, Point(j, i), WHITE_CHESSMAN.Color)

            _draw_left_info(screen, font1, cur_runner, black_win_count, white_win_count)

            if winner:
                print_text(screen, font2, (SCREEN_WIDTH - fwidth) // 2, (SCREEN_HEIGHT - fheight) // 2,
                           winner.Name + '获胜', RED_COLOR)

            pygame.display.flip()


    def _get_next(cur_runner):
        if cur_runner == BLACK_CHESSMAN:
            return WHITE_CHESSMAN
        else:
            return BLACK_CHESSMAN


    def _draw_checkerboard(screen):
        screen.fill(Checkerboard_Color)
        pygame.draw.rect(screen, BLACK_COLOR, (Outer_Width, Outer_Width, Border_Length, Border_Length), Border_Width)
        for i in range(Line_Points):
            pygame.draw.line(screen, BLACK_COLOR,
                             (Start_Y, Start_Y + SIZE * i),
                             (Start_Y + SIZE * (Line_Points - 1), Start_Y + SIZE * i),
                             1)
        for j in range(Line_Points):
            pygame.draw.line(screen, BLACK_COLOR,
                             (Start_X + SIZE * j, Start_X),
                             (Start_X + SIZE * j, Start_X + SIZE * (Line_Points - 1)),
                             1)
        for i in (3, 9, 15):
            for j in (3, 9, 15):
                if i == j == 9:
                    radius = 5
                else:
                    radius = 3
                pygame.gfxdraw.aacircle(screen, Start_X + SIZE * i, Start_Y + SIZE * j, radius, BLACK_COLOR)
                pygame.gfxdraw.filled_circle(screen, Start_X + SIZE * i, Start_Y + SIZE * j, radius, BLACK_COLOR)


    def _draw_chessman(screen, point, stone_color):
        pygame.gfxdraw.aacircle(screen, Start_X + SIZE * point.X, Start_Y + SIZE * point.Y, Stone_Radius, stone_color)
        pygame.gfxdraw.filled_circle(screen, Start_X + SIZE * point.X, Start_Y + SIZE * point.Y, Stone_Radius,
                                     stone_color)

    def _draw_left_info(screen, font, cur_runner, black_win_count, white_win_count):
        _draw_chessman_pos(screen, (SCREEN_HEIGHT + Stone_Radius2, Start_X + Stone_Radius2), BLACK_CHESSMAN.Color)
        _draw_chessman_pos(screen, (SCREEN_HEIGHT + Stone_Radius2, Start_X + Stone_Radius2 * 4), WHITE_CHESSMAN.Color)

        print_text(screen, font, RIGHT_INFO_POS_X, Start_X + 3, '玩家', BLUE_COLOR)
        print_text(screen, font, RIGHT_INFO_POS_X, Start_X + Stone_Radius2 * 3 + 3, '电脑', BLUE_COLOR)

        print_text(screen, font, SCREEN_HEIGHT, SCREEN_HEIGHT - Stone_Radius2 * 8, '战况：', BLUE_COLOR)
        _draw_chessman_pos(screen, (SCREEN_HEIGHT + Stone_Radius2, SCREEN_HEIGHT - int(Stone_Radius2 * 4.5)),
                           BLACK_CHESSMAN.Color)
        _draw_chessman_pos(screen, (SCREEN_HEIGHT + Stone_Radius2, SCREEN_HEIGHT - Stone_Radius2 * 2),
                           WHITE_CHESSMAN.Color)
        print_text(screen, font, RIGHT_INFO_POS_X, SCREEN_HEIGHT - int(Stone_Radius2 * 5.5) + 3, f'{black_win_count} 胜',
                   BLUE_COLOR)
        print_text(screen, font, RIGHT_INFO_POS_X, SCREEN_HEIGHT - Stone_Radius2 * 3 + 3, f'{white_win_count} 胜',
                   BLUE_COLOR)


    def _draw_chessman_pos(screen, pos, stone_color):
        pygame.gfxdraw.aacircle(screen, pos[0], pos[1], Stone_Radius2, stone_color)
        pygame.gfxdraw.filled_circle(screen, pos[0], pos[1], Stone_Radius2, stone_color)

    def _get_clickpoint(click_pos):
        pos_x = click_pos[0] - Start_X
        pos_y = click_pos[1] - Start_Y
        if pos_x < -Inside_Width or pos_y < -Inside_Width:
            return None
        x = pos_x // SIZE
        y = pos_y // SIZE
        if pos_x % SIZE > Stone_Radius:
            x += 1
        if pos_y % SIZE > Stone_Radius:
            y += 1
        if x >= Line_Points or y >= Line_Points:
            return None

        return Point(x, y)


    class AI:
        def __init__(self, line_points, chessman):
            self._line_points = line_points
            self._my = chessman
            self._opponent = BLACK_CHESSMAN if chessman == WHITE_CHESSMAN else WHITE_CHESSMAN
            self._checkerboard = [[0] * line_points for _ in range(line_points)]

        def get_opponent_drop(self, point):
            self._checkerboard[point.Y][point.X] = self._opponent.Value

        def AI_drop(self):
            point = None
            score = 0
            for i in range(self._line_points):
                for j in range(self._line_points):
                    if self._checkerboard[j][i] == 0:
                        _score = self._get_point_score(Point(i, j))
                        if _score > score:
                            score = _score
                            point = Point(i, j)
                        elif _score == score and _score > 0:
                            r = random.randint(0, 100)
                            if r % 2 == 0:
                                point = Point(i, j)
            self._checkerboard[point.Y][point.X] = self._my.Value
            return point

        def _get_point_score(self, point):
            score = 0
            for os in offset:
                score += self._get_direction_score(point, os[0], os[1])
            return score

        def _get_direction_score(self, point, x_offset, y_offset):
            count = 0
            _count = 0
            space = None
            _space = None
            both = 0
            _both = 0

            flag = self._get_stone_color(point, x_offset, y_offset, True)
            if flag != 0:
                for step in range(1, 6):
                    x = point.X + step * x_offset
                    y = point.Y + step * y_offset
                    if 0 <= x < self._line_points and 0 <= y < self._line_points:
                        if flag == 1:
                            if self._checkerboard[y][x] == self._my.Value:
                                count += 1
                                if space is False:
                                    space = True
                            elif self._checkerboard[y][x] == self._opponent.Value:
                                _both += 1
                                break
                            else:
                                if space is None:
                                    space = False
                                else:
                                    break
                        elif flag == 2:
                            if self._checkerboard[y][x] == self._my.Value:
                                _both += 1
                                break
                            elif self._checkerboard[y][x] == self._opponent.Value:
                                _count += 1
                                if _space is False:
                                    _space = True
                            else:
                                if _space is None:
                                    _space = False
                                else:
                                    break
                    else:
                        if flag == 1:
                            both += 1
                        elif flag == 2:
                            _both += 1

            if space is False:
                space = None
            if _space is False:
                _space = None

            _flag = self._get_stone_color(point, -x_offset, -y_offset, True)
            if _flag != 0:
                for step in range(1, 6):
                    x = point.X - step * x_offset
                    y = point.Y - step * y_offset
                    if 0 <= x < self._line_points and 0 <= y < self._line_points:
                        if _flag == 1:
                            if self._checkerboard[y][x] == self._my.Value:
                                count += 1
                                if space is False:
                                    space = True
                            elif self._checkerboard[y][x] == self._opponent.Value:
                                _both += 1
                                break
                            else:
                                if space is None:
                                    space = False
                                else:
                                    break
                        elif _flag == 2:
                            if self._checkerboard[y][x] == self._my.Value:
                                _both += 1
                                break
                            elif self._checkerboard[y][x] == self._opponent.Value:
                                _count += 1
                                if _space is False:
                                    _space = True
                            else:
                                if _space is None:
                                    _space = False
                                else:
                                    break
                    else:
                        if _flag == 1:
                            both += 1
                        elif _flag == 2:
                            _both += 1

            score = 0
            if count == 4:
                score = 10000
            elif _count == 4:
                score = 9000
            elif count == 3:
                if both == 0:
                    score = 1000
                elif both == 1:
                    score = 100
                else:
                    score = 0
            elif _count == 3:
                if _both == 0:
                    score = 900
                elif _both == 1:
                    score = 90
                else:
                    score = 0
            elif count == 2:
                if both == 0:
                    score = 100
                elif both == 1:
                    score = 10
                else:
                    score = 0
            elif _count == 2:
                if _both == 0:
                    score = 90
                elif _both == 1:
                    score = 9
                else:
                    score = 0
            elif count == 1:
                score = 10
            elif _count == 1:
                score = 9
            else:
                score = 0

            if space or _space:
                score /= 2

            return score

        def _get_stone_color(self, point, x_offset, y_offset, next):
            x = point.X + x_offset
            y = point.Y + y_offset
            if 0 <= x < self._line_points and 0 <= y < self._line_points:
                if self._checkerboard[y][x] == self._my.Value:
                    return 1
                elif self._checkerboard[y][x] == self._opponent.Value:
                    return 2
                else:
                    if next:
                        return self._get_stone_color(Point(x, y), x_offset, y_offset, False)
                    else:
                        return 0
            else:
                return 0


    if __name__ == '__main__':
        main()