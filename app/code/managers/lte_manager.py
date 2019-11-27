import serial
import time
#import datetime

# TODO specify other params such as data size
# move into own function
s = serial.Serial("/dev/ttyS0", 115200)
s.flushInput()

#TODO move send_command out of SMS section

#def setup_lte_connection():#
#       s = serial.Serial("/dev/ttyS0", 115200)
#       s.flushInput()
#       send_command("ATE0\r\n")
#       return s

#s = setup_lte_connection()

## SMS
default_number = "+13605507462"
default_message = "hi"

def check_sms_mode():
        send_command("AT+CMGF?\r\n")

def send_command(command=None):
        # take user input if no command supplied yet
        if command == None:
                command = input("input: ")
        # SIM7000 understands ASCII
        command = command.encode("ASCII")
        s.write(command)
        time.sleep(0.5)
        if s.inWaiting():
                response = s.read(s.inWaiting())
                response = response.decode()
                return response

def set_echo(mode=0):
        return send_command("ATE" + str(mode) + "\r\n")

#### GPS
def get_gps_power():
        response = send_command("AT+CGNSPWR?\r\n")
        if response.find("CGNSPWR: 0") == -1:
                return 1
        else:
                return 0

def turn_gps_on():
        return send_command("AT+CGNSPWR=1\r\n")

def turn_gps_off():
        return send_command("AT+CGNSPWR=0\r\n")

def get_gps_loc():
        reply = send_command("AT+CGNSINF\r\n")
        reply = str(reply)
        info = reply.split(",")
        print(info)
        lat = info[3]
        lon = info[4]
        if lat == "" or lon == "":
                return None
        return lat + "," + lon

def send_sms(number=default_number, message=default_message):
        c = "AT+CMGS=\"" + number + "\"\r"
        send_command(c)
        send_command(message)
        # ASCII character 26 is CTRL^Z, and for AT+CMGS signfies that the message is complete and should be sent
        e = chr(26)
        send_command(e)


#TODO implement the two below
def list_sms():
        send_command("AT+CMGL=\"ALL\",1\r\n")

def read_sms():
        pass

def lte_insert_data(data):
        device_id = str(data[0])
        time_stamp = data[1]
        count = str(data[2])
        sms = "updateid" + device_id + "idendtime" + time_stamp + "timeendcount" + count + "countend"
        send_sms("+12062600742", sms)

def setup_sms(mode=1):
        # set mode between PDU or text
        command = "AT+CMGF=" + str(mode) + "\r\n"
        send_command(command)

## HTTP
def start_http():
        # terminate service if still running
        send_command("AT+HTTPTERM\r\n")
        # if receive OK
        # initialize new service
        send_command("AT+HTTPINIT\r\n")
        # set CID parameter - not sure what CID is
        send_command("AT+HTTPPARA=\"CID\",1\r\n")

def end_http():
        send_command("AT+HTTPTERM\r\n")

#TODO general function for setting up HTTP params for either POST or GET
#TODO general function that performs POST or GET depending on one parameter
def http_request(method=None, url=None, userdata=None, content=None, data=None):
        # for testing
        method = "GET"
        url = "www.sim.com"
        userdata = None
        content = None
        data = None

        # set url to send request to
        send_command("AT+HTTPPARA=\"URL\",\"" + url + "\"\r\n")

        # set to  GET
        if method.lower() == "get":
                send_command("AT+HTTPACTION=0\r\n")
        # OR set to POST
        elif method.lower() == "post":
                send_command("AT+HTTPACTION=1\r\n")

# TODO implement GET

def post(url=None, userdata=None, content=None, data=None):
        # set action to post
        send_command("AT+HTTPACTION=1\r\n")
        send_command("AT+HTTPACTION=?\r\n")
