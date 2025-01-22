import pygame
import mediapipe as mp
import cv2
import numpy as np
import threading

class HandControl:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)  # Mở webcam
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils
        self.direction = 0  # 0: Không di chuyển, -1: Trái, 1: Phải

        self.running = True
        self.thread = threading.Thread(target=self.process_video)
        self.thread.start()

    def process_video(self):
        while self.running:
            success, frame = self.cap.read()
            if not success:
                break

            # Chuyển đổi BGR sang RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Lấy vị trí các landmark chính
                    wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
                    index_finger = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]

                    # Tính toán khoảng cách theo trục x để xác định hướng
                    if wrist.x - index_finger.x > 0.05:
                        self.direction = -1  # Sang trái
                    elif index_finger.x - wrist.x > 0.05:
                        self.direction = 1  # Sang phải
                    else:
                        self.direction = 0  # Không di chuyển

                    # Vẽ bàn tay lên frame (tùy chọn để debug)
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

            # Hiển thị frame (để kiểm tra nếu cần)
            cv2.imshow("Hand Tracking", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False
                break

    def stop(self):
        self.running = False
        self.cap.release()
        cv2.destroyAllWindows()

# Lớp game Capy đã được định nghĩa trước
class Capy:
    def __init__(self):
        pygame.init()
        self.WIDTH = 500
        self.HEIGHT = 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Capypara")
        self.clock = pygame.time.Clock()
        self.running = True

        # Nhân vật
        self.player_x = 240
        self.player_y = 700
        self.x_speed = 5

        # Hand control
        self.hand_control = HandControl()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Di chuyển nhân vật dựa trên MediaPipe input
            if self.hand_control.direction == -1:  # Trái
                self.player_x -= self.x_speed
            elif self.hand_control.direction == 1:  # Phải
                self.player_x += self.x_speed

            # Giới hạn nhân vật trong màn hình
            self.player_x = max(0, min(self.WIDTH - 50, self.player_x))

            # Cập nhật giao diện
            self.screen.fill((135, 206, 235))  # Màu nền xanh trời
            pygame.draw.rect(self.screen, (255, 0, 0), (self.player_x, self.player_y, 50, 50))  # Nhân vật là hình vuông
            pygame.display.flip()
            self.clock.tick(60)

        # Dừng MediaPipe
        self.hand_control.stop()
        pygame.quit()

# Chạy game
if __name__ == "__main__":
    game = Capy()
    game.run()
