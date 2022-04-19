import cv2
import numpy as np
import uuid
import json
 
class FireDefault:
    """
        Класс первоначальной настройки\n
        Параметры ввода:\n
        id - None\n
        \tlower - [18, 50, 50]\n
        \tupper - [35, 255, 255],\n\n
        где id - является не обязательным параметром, lower и upper за определение нижнего и верхнего цвета
    """
    def __init__(self,id=None, lower=[],upper=[]) -> None:
        if not id:
            self.id = uuid.uuid4().__str__()
        else: self.id= id
        self.lower = lower
        self.upper = upper

    def toString(self) -> str:
        """Преобзование класса в JSON строку"""
        return {
            "id":self.id,
            "lower":self.lower,
            "upper":self.upper
        }

    def __str__(self) -> str:
        """Преобразование класса в строку"""
        return str(self.toString())

    def get(self)->list:
        """
            Получениче lower и upper\n
            [lower, upper]
        """
        return [
            self.lower,
            self.upper
        ]

class SettingFire:
    def __init__(self) -> None:
        self.fire = []

    def __str__(self) -> str:
        return str(
            [str(i) for i in self.fire]
        )
    def toString(self)->str:
        return [i.toString() for i in self.fire]

    def add(self, lower:list, upper:list)-> list:
        if min(lower)<0 or max(lower)>255:
            raise Exception("")
        self.fire.append(FireDefault(None, lower, upper))
        return self.fire
    
    def delete(self, id:str)->list:
        for item in self.fire:
            if item.id == id:
                self.fire.remove(item)
                return self.fire
    
    def save(self, path="./file.json"):
        with open(path,"w", encoding="utf-8") as file:
            item = self.toString()
            file.write(json.dumps(item, indent=4))
        return path
    
    
    def open(self, path="./file.json"):
        with open(path,"r", encoding="utf-8") as file:
            try:
                items = json.loads(file.read())
                for item in items:
                    self.fire.append(FireDefault(item["id"], item["lower"], item["upper"]))
            except:
                pass
        return self.fire


class Fire(SettingFire):
    def __init__(self, path:str) -> None:
        if "mp4" in path:
            self.video  = cv2.VideoCapture(path)
        else:
            self.video  = cv2.imread(path)
        super().__init__()

    def find(self, start_video=False):
        while True:
            try:
                tt = True

                (grabbed, frame) = self.video.read()
            except:
                tt =False
                grabbed = True 
                frame = self.video

            if not grabbed:
                break
            if tt:
                blur = cv2.GaussianBlur(frame, (21, 21), 0)
                hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
            else:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            for item in self.fire:
                (lower, upper) = item.get()
                lower = np.array(lower, dtype="uint8")
                upper = np.array(upper, dtype="uint8")
                mask = cv2.inRange(hsv, lower, upper)
                output = cv2.bitwise_and(frame, hsv, mask=mask)
                thresh = cv2.inRange(hsv, lower, upper)
                contours,_ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                height, width = output.shape[:2]
                count = 0
                for i in contours:
                    dddd = cv2.contourArea(i)
                    
                    if dddd>350:
                        count+=dddd
                        cv2.drawContours( output, contours, -1, [255,37,37], 3,  cv2.LINE_AA)
                procent = 100*count/ (height*width)
                if (procent>30):
                    yield {
                        "procent":procent if procent<100 else 100
                    }

                if start_video:
                    cv2.imshow("output", output)

                # if procent > 20:
                #     yield True
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            if not tt:
                break
        
        cv2.destroyAllWindows()
        try:
            self.video.release()
        except:
            pass