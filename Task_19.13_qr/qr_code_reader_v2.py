import cv2
import qrcode

# Initialize the camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Stop")
        continue

    # Display the camera feed
    cv2.imshow("Camera Feed", frame)

    # Initialize a QRCode detector
    detector = cv2.QRCodeDetector()

    # Detect the QR code
    retval, decoded_info, points, straight_qrcode = detector.detectAndDecodeMulti(frame)

    if retval:
        if len(decoded_info) > 0:
            detected_qr_str = decoded_info[0]
        else:
            detected_qr_str = "No QR code detected"

        if detected_qr_str == "Shreenath Siriyala 9075009459":
            print("Hi")
        else:
            print("Stop")

        print("Detected QR Code: " + detected_qr_str)

    else:
        print("Stop")

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
