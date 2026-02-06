import cv2
import numpy as np
import time
from mss import mss
from ultralytics import YOLO
import pyautogui

monitor = {"top": 200, "left": 100, "width": 640, "height": 480}

model = YOLO(r'runs/detect/dino_v1/weights/best.pt')

def main():
    sct = mss()
    pTime = 0
    print("Ekran yakalama başladı... Çıkmak için 'q' bas.")

    game_ready = False 

    NORMAL_JUMP_DIST = 170 
    
    WIDE_OBSTACLE_WIDTH = 75   
    BIRD_JUMP_DIST = 190
    LATE_JUMP_DIST = 160
    
    GAP_THRESHOLD = 150        
    EARLY_JUMP_DIST = 180 

    while True:
        screenshot = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        results = model(frame, stream=True, verbose=False, conf=0.5)

        cacti = [] 
        birds = []
        dino_x = 0 

        for r in results:
            frame = r.plot()
            
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                cls_id = int(box.cls[0].item())
                name = r.names[cls_id]
                
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                if name == "dinosaur":
                    dino_x = x2 
                    if not game_ready:
                        game_ready = True
                        pyautogui.press('space')
                
                elif name == "cactus":
                    width = x2 - x1
                    cacti.append({'x1': x1, 'x2': x2, 'w': width})
                
                elif name == "bird":
                    birds.append({'x1': x1, 'y1': y1})

        if game_ready:
            
            cacti.sort(key=lambda c: c['x1'])

            if len(cacti) > 0:
                closest = cacti[0]     
                dist = closest['x1']   

                trigger_point = NORMAL_JUMP_DIST
                jump_reason = "Normal"
                should_long_press = False

                
                
                if len(cacti) > 1:
                    second_cactus = cacti[1]
                    gap = second_cactus['x1'] - closest['x2']
                    
                    if gap < GAP_THRESHOLD:
                        trigger_point = EARLY_JUMP_DIST 
                        jump_reason = "Seri Engel"
                        should_long_press = True 
                
                
                elif closest['w'] > WIDE_OBSTACLE_WIDTH:
                    trigger_point = LATE_JUMP_DIST 
                    jump_reason = "Genis (3'lu)"

                cv2.putText(frame, f"Kaktus Hedef: <{trigger_point}px", (100, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

                if dist < trigger_point:
                    if should_long_press:
                        
                        pyautogui.keyDown('space')
                        time.sleep(0.12) 
                        pyautogui.keyUp('space')
                    else:
                        pyautogui.press('space')
                        
                    print(f"ZIPLAMA: {jump_reason} | Mesafe: {dist} | Uzun Basma: {should_long_press}")

            
            for bird in birds:
                if bird['x1'] < BIRD_JUMP_DIST:
                    if bird['y1'] > 195:
                        pyautogui.press('down')
                        print(f"EGIL: Alcak Kus (y={bird['y1']})")
                    else:
                        pyautogui.press('space')
                        print(f"ZIPLA: Yuksek Kus (y={bird['y1']})")

        cv2.putText(frame, f"FPS: {int(fps)}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Screen Perception (Sim)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()