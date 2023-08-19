import cv2
import numpy as np
import nonMaximanSuppression as nms

def leerCamarasDisponibles():
    index = 0
    array = []
    while True:
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if not cap.read()[0]:
            break
        else:
            array.append(str(index))
        cap.release()
        index += 1
    return array

def capturarImagenShow(camara):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    leido, frame = cap.read()
    cv2.imwrite("capture.jpg", frame)
    height, width, bytesPerComponent = frame.shape
    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame)
    bytesPerLine = 3 * width
    return frame, height, width, bytesPerLine

def capturarImagenSim(ruta):
    frame = cv2.imread(ruta)
    cv2.imwrite("capture.jpg", frame)
    height, width, bytesPerComponent = frame.shape
    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame)
    bytesPerLine = 3 * width
    return frame, height, width, bytesPerLine

def convertirImagen(frame):
    height, width, bytesPerComponent = frame.shape
    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame)
    bytesPerLine = 3 * width
    return frame, height, width, bytesPerLine

def extractColor(frame, r):
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    imagenNueva = frameHSV[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    altura, ancho = imagenNueva.shape[:2]

    H=[]
    S=[]
    V=[]

    for i in range(altura):
        for j in range(ancho):
            pixel = imagenNueva[i,j]
            H.append(pixel[0])
            S.append(pixel[1])
            V.append(pixel[2])

    hMin = min(H)
    hMax = max(H)
    sMin = min(S)
    sMax = max(S)
    vMin = min(V)
    vMax = max(V)

    bajo = np.array([hMin, sMin, vMin], np.uint8)
    alto = np.array([hMax, sMax, vMax], np.uint8)

    mask = cv2.inRange(frameHSV, bajo, alto)
    total = 0
    altura, ancho = mask.shape[:2]
    for i in range(altura):
        for j in range(ancho):
            pixel = mask[i,j]
            if pixel == 255:
                total +=1
                frame[i,j] = (0,255,0)

    return bajo, alto, total

def testColor(porcentajeMeta, frameX, bajo, alto, totalX):
    frame = frameX.copy()
    frameHSV = cv2.cvtColor(frame, bajo, alto)

    mask = cv2.inRange(frameHSV, bajo, alto)
    total = 0
    altura, ancho = mask.shape[:2]

    for i in range(altura):
        for j in range(ancho):
            pixel = mask[i,j]
            if pixel == 255:
                total += 1
                frame[i,j] = (0,255,0)

    multi = total * 100
    porcentaje = multi / totalX

    if porcentaje > 100:
        porcentaje = 100

    if porcentaje < porcentajeMeta:
        res = ("NG", porcentaje)
    else:
        res = ('OK', porcentaje)
    return res

def testPlantilla(img_rgbx, r, totalX, imgTestShow, imgMaster):
    global box
    total = 0
    img_rgb = img_rgbx.copy()
    img_grayT = cv2.cvtColor(imgMaster, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.cvtColor(img_rgbx, cv2.COLOR_BGR2GRAY)
    template = img_grayT[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray,template, cv2.TM_CCORR_NORMED)
    threshold = 0.93
    rectangulos = np.where(res > threshold)
    boxes =[]
    for pt in zip(*rectangulos[::-1]):
        box = (pt[0],pt[1],pt[0]+w,pt[1]+h)
        boxes.append(box)

    boxes = np.array(boxes)
    boxes = nms.non_max_suppression_fast(boxes, 0.3)

    for box in boxes:
        cv2.rectangle(imgTestShow, (box[0], box[1]), (box[2], box[3]), (255,0,0), 2)
        total += 1

    if total == totalX:
        res = ('OK',total)
    else:
        res = ('NG', total)

    return res, imgTestShow