import pygame
import random


class Capy:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.x = 0

        self.WIDTH = 500
        self.HEIGHT = 800
        self.fps = 60
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        pygame.display.set_caption("Capypara")

        self.bg = (135, 206, 235)
        self.clock = pygame.time.Clock()
        self.huge_font = pygame.font.Font('assets/Terserah.ttf', 42)
        self.font = pygame.font.Font('assets/Terserah.ttf', 24)
        self.huge_textfont = pygame.font.Font('assets/Arial.ttf', 70)
        self.textfont = pygame.font.Font('assets/Arial.ttf', 24)
        self.game_over = False
        self.rocks = [[200, 100, 1], [50, 330, 2], [350, 330, 3], [200, 670, 1]]
        self.rock_images = [pygame.transform.scale(pygame.image.load(f'assets/rocks/r{i}.png'), (100, 70)) for i in
                             range(1, 4)]

        self.player_x = 240
        self.player_y = 40
        self.capy = pygame.transform.flip(pygame.transform.scale(pygame.image.load('assets/capy.png'), (34, 90)),
                                             False, True)
        self.bg_image = pygame.transform.scale(pygame.image.load('assets/background.png'), (self.WIDTH, self.HEIGHT))
        self.capy_left = pygame.transform.rotate(self.capy, -10)
        self.capy_right = pygame.transform.rotate(self.capy, 10)

        self.direction = -1
        self.y_speed = 0
        self.gravity = 0.1
        self.x_speed = 3
        self.x_direction = 0

        self.score = 0
        self.total_distance = 0
        self.high_score = self.load_high_score()

        pygame.mixer.music.load('assets/theme.mp3')
        self.bounce_sound = pygame.mixer.Sound('assets/bounce.mp3')
        self.end_sound = pygame.mixer.Sound('assets/game_over.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)
        self.show_question = False
        self.question_answered = False

        # Thêm câu hỏi và các đáp án
        self.question_text = "Ai đẹp trai nhất?"
        self.answers = ["A. Tris", "B. Tri", "C. Tr", "D. T"]
        self.correct_answer = "A. Tris"  # Đáp án đúng
        self.health = 3  # Nhân vật có 3 máu ban đầu

    def draw_question(self):
        # Vẽ khung bảng câu hỏi
        pygame.draw.rect(self.screen, (255, 255, 255), (50, 200, 400, 300), border_radius=10)
        pygame.draw.rect(self.screen, (0, 0, 0), (50, 200, 400, 300), 3, border_radius=10)

        # Vẽ câu hỏi
        question_render = self.textfont.render(self.question_text, True, (0, 0, 0))
        self.screen.blit(question_render, (70, 220))

        # Vẽ các nút đáp án
        for i, answer in enumerate(self.answers):
            print(answer)
            x = 70
            y = 270 + i * 50
            pygame.draw.rect(self.screen, (200, 200, 200), (x, y, 360, 40), border_radius=5)
            pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 360, 40), 2, border_radius=5)
            answer_render = self.textfont.render(str(i+1)+"/   "+str(answer), True, (0, 0, 0))
            self.screen.blit(answer_render, (x + 10, y + 10))

    def load_high_score(self):
        with open('high_scores.txt', 'r') as file:
            return int(file.readline())

    def save_high_score(self):
        with open('high_scores.txt', 'w') as file:
            file.write(str(self.high_score))

    def draw_rocks(self):
        platforms = []
        for rock in self.rocks:
            image = self.rock_images[rock[2] - 1]
            platform = pygame.rect.Rect((rock[0] + 5, rock[1] + 40), (120, 10))
            self.screen.blit(image, (rock[0], rock[1]))
            pygame.draw.rect(self.screen, 'gray', [rock[0] + 15, rock[1] + 40, 30, 3])
            platforms.append(platform)
        return platforms

    def draw_player(self):
        if self.x_direction == -1:
            player_img = self.capy_left  # Nghiêng sang trái
        elif self.x_direction == 1:
            player_img = self.capy_right  # Nghiêng sang phải
        else:
            player_img = self.capy  # Bình thường

        self.screen.blit(player_img, (self.player_x, self.player_y))
        return pygame.rect.Rect((self.player_x + 7, self.player_y + 40), (36, 10))

    def update_objects(self):
        lowest_rock = 0
        update_speed = 10

        # Giới hạn số lượng rock tối đa
        max_rocks = 4

        # Di chuyển các rock lên trên nếu người chơi ở gần đáy màn hình
        if self.player_y > 200:
            self.player_y -= update_speed
            for rock in self.rocks:
                rock[1] -= update_speed
                if rock[1] > lowest_rock:
                    lowest_rock = rock[1]

            # Xóa các rock ra khỏi màn hình
            self.rocks = [rock for rock in self.rocks if rock[1] > -70]

            # Spawn rock mới nếu cần
            if len(self.rocks) < max_rocks and lowest_rock < 750:
                # Số lượng rock spawn mới (1 hoặc 2)
                num_rocks = random.randint(1, 2)

                if num_rocks == 1:
                    # Spawn một rock ở vị trí ngẫu nhiên
                    new_rock = [
                        random.randint(0, self.WIDTH - 70),  # X
                        random.randint(self.HEIGHT + 100, self.HEIGHT + 300),  # Y
                        random.randint(1, 3)  # Loại rock
                    ]
                    self.rocks.append(new_rock)
                else:
                    # Spawn hai rock ở hai nửa màn hình
                    x1, y1, type1 = random.randint(0, self.WIDTH // 2 - 70), random.randint(self.HEIGHT + 100,
                                                                                            self.HEIGHT + 300), random.randint(
                        1, 3)
                    x2, y2, type2 = random.randint(self.WIDTH // 2 + 70, self.WIDTH - 70), random.randint(
                        self.HEIGHT + 100, self.HEIGHT + 300), random.randint(1, 3)
                    self.rocks.extend([[x1, y1, type1], [x2, y2, type2]])

    def reset_game(self):
        self.game_over = False
        self.player_x = 240
        self.player_y = 40
        self.direction = -1
        self.y_speed = 0
        self.x_direction = 0
        self.score = 0
        self.total_distance = 0
        self.rocks = [[200, 100, 1], [50, 330, 2], [350, 330, 3], [200, 670, 1]]
        pygame.mixer.music.play(-1)

    def draw_end_screen(self):
        self.screen.fill((0, 0, 0))  # Xóa màn hình bằng màu đen
        game_over_text = self.huge_font.render("GAME OVER", True, (255, 0, 0))
        restart_text = self.textfont.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
        score_text = self.font.render(f'Your Score: {self.score}', True, (255, 255, 255))
        high_score_text = self.font.render(f'High Score: {self.high_score}', True, (255, 255, 255))

        # Hiển thị các dòng text
        self.screen.blit(game_over_text, (self.WIDTH // 2 - game_over_text.get_width() // 2, 200))
        self.screen.blit(restart_text, (self.WIDTH // 2 - restart_text.get_width() // 2, 300))
        self.screen.blit(score_text, (self.WIDTH // 2 - score_text.get_width() // 2, 400))
        self.screen.blit(high_score_text, (self.WIDTH // 2 - high_score_text.get_width() // 2, 450))

    def generate_simple_math_question(self):
        num_count = random.randint(2, 3)  # Số lượng số ngẫu nhiên (2 hoặc 3 số)
        numbers = [random.randint(1, 10) for _ in range(num_count)]
        operators = ['+', '-', '*']
        operations = [random.choice(operators) for _ in range(num_count - 1)]

        # Ghép các số và toán tử thành biểu thức
        expression = f"{numbers[0]}"
        for i in range(1, num_count):
            expression += f" {operations[i - 1]} {numbers[i]}"

        correct_answer = eval(expression)

        # Tạo đáp án bao gồm 1 đáp án đúng và 3 đáp án sai
        answers = [correct_answer]
        while len(answers) < 4:
            wrong_answer = correct_answer + random.choice([-2, -1, 1, 2])
            if wrong_answer not in answers:  # Đảm bảo không trùng lặp đáp án
                answers.append(wrong_answer)

        random.shuffle(answers)

        return expression, answers, correct_answer

    def update_score(self):
        self.total_distance += self.y_speed
        self.score = round(self.total_distance / 100)

    def draw_texts(self):
        score_text = self.font.render(f'Score: {self.score}', True, 'black')
        high_score_text = self.font.render(f'High Score: {self.high_score}', True, 'black')
        self.screen.blit(score_text, (10, self.HEIGHT - 70))
        self.screen.blit(high_score_text, (10, self.HEIGHT - 40))
        if self.game_over:
            end_text = self.huge_font.render("Capypara!", True, 'black')
            end_text2 = self.font.render('Game Over: Press Enter to Restart', True, 'black')
            self.screen.blit(end_text, (70, 20))
            self.screen.blit(end_text2, (60, 80))

    def check_answer(self, index):
        self.question_answered = True
        self.show_question = False
        if self.answers[index] == self.correct_answer:
            print("Đúng rồi!")
            self.player_y += 50  # Nhân vật nhảy lên
        else:
            print("Sai rồi!")
            self.health -= 1  # Mất máu
            self.player_y += 50  # Nhân vật rơi xuống
            if self.health <= 0:
                self.game_over = True
                pygame.mixer.Sound.play(self.end_sound)  # Chơi âm thanh game over

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if self.game_over:  # Xử lý khi game kết thúc
                if event.key == pygame.K_r:  # Nhấn "R" để chơi lại
                    self.reset_game()
                elif event.key == pygame.K_q:  # Nhấn "Q" để thoát game
                    pygame.quit()
                    exit()
            else:
                if event.key == pygame.K_LEFT:
                    self.x_direction = -1
                elif event.key == pygame.K_RIGHT:
                    self.x_direction = 1

                # Xử lý phím chọn đáp án khi có câu hỏi
                if self.show_question and event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    # Lấy chỉ số đáp án dựa trên phím nhấn (K_1 -> 0, K_2 -> 1, ...)
                    answer_index = event.key - pygame.K_1
                    if 0 <= answer_index < len(self.answers):  # Đảm bảo chỉ số hợp lệ
                        self.check_answer(answer_index)  # Kiểm tra đáp án

        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                self.x_direction = 0

        # Xử lý click chuột khi có câu hỏi
        if self.show_question and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i, answer in enumerate(self.answers):
                x, y = 70, 270 + i * 50
                if x <= mouse_x <= x + 360 and y <= mouse_y <= y + 40:
                    self.check_answer(i)  # Kiểm tra đáp án khi click chuột

    def check_collisions(self, rock_platforms):
        on_rock = False
        for platform in rock_platforms:
            if self.direction == -1 and pygame.Rect.colliderect(platform,
                                                                pygame.Rect(self.player_x + 7, self.player_y + 40, 36,
                                                                            10)):
                self.player_y = platform.top - 40  # Đặt nhân vật lên trên đám mây
                self.y_speed = 0  # Dừng vận tốc rơi
                on_rock = True

                # Tạo câu hỏi mới
                self.question_text, self.answers, self.correct_answer = self.generate_simple_math_question()
                print(self.question_text, self.answers, self.correct_answer)
                self.show_question = True  # Hiển thị câu hỏi
                break

        if not on_rock:
            self.y_speed += self.gravity  # Tiếp tục cho nhân vật rơi nếu không đứng trên mây

    def run_game(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Xóa màn hình
            self.screen.blit(self.bg_image, (0, 0))  # Vẽ ảnh nền
            self.clock.tick(self.fps)

            if self.game_over:  # Kiểm tra trạng thái game
                self.draw_end_screen()  # Hiển thị màn hình kết thúc
            else:
                health_text = self.huge_textfont.render(f"{self.health * '$'}", True, (255, 0, 0))
                self.screen.blit(health_text, (10, 10))
                if self.show_question:
                    self.draw_question()  # Hiển thị bảng câu hỏi
                else:
                    rock_platforms = self.draw_rocks()
                    player_rect = self.draw_player()
                    self.update_objects()
                    self.update_score()
                    self.draw_texts()
                    self.check_collisions(rock_platforms)

                    if not self.game_over:
                        self.y_speed = min(self.y_speed + self.gravity, 10)
                        self.player_y += self.y_speed
                        self.direction = 1 if self.y_speed < 0 else -1
                        self.player_x += self.x_speed * self.x_direction
                        if self.player_x > self.WIDTH:
                            self.player_x = -30
                        elif self.player_x < -50:
                            self.player_x = self.WIDTH - 20

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_input(event)

            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    game = Capy()
    game.run_game()
