import cv2
import pyrealsense2 as rs
import qrcode
import numpy as np
import serial


# Define the serial port and baud rate
serial_port = '/dev/ttyUSB0'  # Update with your actual serial port
baud_rate = 115200

# Create a serial object
ser = serial.Serial(serial_port, baud_rate, timeout=1)


# Function to set the motor speeds
def set_motor_speeds(motor_ctrl_code):
    command = 'L{} R{}\n'.format(motor_ctrl_code, 0)
    ser.write(command.encode())


# Initialize the Intel RealSense camera
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

profile = pipeline.start(config)

while True:
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()

    if not color_frame:
        print("Stop")
        continue

    # Convert the color frame to a numpy array
    frame = np.asanyarray(color_frame.get_data())

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
            set_motor_speeds(1)
            print("Move Forward")
        else:
            set_motor_speeds(0)
            print("Stop")

        print("Detected QR Code: " + detected_qr_str)

    else:
        print("Stop")

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the OpenCV window
pipeline.stop()
cv2.destroyAllWindows()
