import cv2
import numpy as np

thresh = 25
max_diff = 5

a, b = None, None

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

if cap.isOpened():
    ret, a = cap.read()

    while ret:
        ret, b = cap.read()
        if not ret:
            break

        a_gray = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
        b_gray = cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)

        diff1 = cv2.absdiff(a_gray, b_gray)
        ret, diff_t = cv2.threshold(diff1, thresh, 255, cv2.THRESH_BINARY)

        k = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        diff = cv2.morphologyEx(diff_t, cv2.MORPH_OPEN, k)

        diff_cnt = cv2.countNonZero(diff)
        if diff_cnt > max_diff:
            nzero = np.nonzero(diff)
            cv2.rectangle(b, (min(nzero[1]), min(nzero[0])),
                          (max(nzero[1]), max(nzero[0])), (0, 255, 0), 2)

            cv2.putText(b, "Motion detected!!", (10, 30),
                                                 cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255))

        cv2.imshow('motion', b)

        a = b

        if cv2.waitKey(1) & 0xFF == 27:
            break
