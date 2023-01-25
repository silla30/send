from flask import Flask, request, render_template
import serial
import time
import re


def connectPhone(portcom):
    try:
        phone = serial.Serial(portcom,  115200, timeout=2, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, xonxoff=False, rtscts=False,
                              dsrdtr=False, writeTimeout=2)
        return phone
    except:
        pass


def disconnectPhone():
    try:
        connectPhone().close()
    except:
        pass


def read_until(ser, group, terminator='\n'):
    try:
        print('reading {}...'.format(ser.name))
        resp = ''
        time.sleep(3)
        # If the string is not terminated
        while not (resp.endswith(terminator) or resp.endswith('\r')):
            tmp = ser.readall()   # Read and store in a temp variable
            if not tmp:
                return resp  # timeout occured
            resp += tmp.decode()
            example1 = re.search(
                r'(AT\+[\s\S]*?CUSD:[^\"\"]*\")([^\"]*)', resp)
        ser.close()
        print(ser.isOpen())
        # disconnectPhone()
        print(ser.isOpen())
        return example1.group(group)

    except Exception as e:
        print(e)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/send', methods=['GET','POST'])
def send_sms():
    if request.method == 'POST':
       phone = connectPhone('COM6')
       phone.write('AT+CUSD=1,"*101#",15\r'.encode())
       time.sleep(5)
       return(read_until(phone, 2))
    return render_template('send.html')


if __name__ == '__main__':
    app.run(debug=True)
