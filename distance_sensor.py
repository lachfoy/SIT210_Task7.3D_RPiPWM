import RPi.GPIO as GPIO
import time

try:
	GPIO.setmode(GPIO.BOARD)
	PIN_TRIGGER = 7
	PIN_ECHO = 11
	PIN_BUZZER = 29

	GPIO.setup(PIN_TRIGGER, GPIO.OUT)
	GPIO.setup(PIN_ECHO, GPIO.IN)
	GPIO.setup(PIN_BUZZER, GPIO.OUT, initial=GPIO.LOW)

	GPIO.output(PIN_TRIGGER, GPIO.LOW)

	# Sensor settling
	time.sleep(2)

	pwm = GPIO.PWM(PIN_BUZZER, 100)
	pwm.start(0)

	while(1):
		# Send trigger signal
		GPIO.output(PIN_TRIGGER, GPIO.HIGH)
		time.sleep(0.00001)
		GPIO.output(PIN_TRIGGER, GPIO.LOW)

		# Capture pulse echo start and end
		while GPIO.input(PIN_ECHO)==0:
			pulse_start_time = time.time()
		while GPIO.input(PIN_ECHO)==1:
			pulse_end_time = time.time()

		# Calculate distance in cm
		pulse_duration = pulse_end_time - pulse_start_time
		distance = round(pulse_duration * 17150, 2)

		print(distance)

		# Buzzer depends on distance
		if (distance <= 50):
			pwm.ChangeFrequency(6 - distance/10)
			pwm.ChangeDutyCycle(50)
			time.sleep(0.5)
		else:
			pwm.ChangeDutyCycle(50)
		time.sleep(1)

except KeyboardInterrupt:
	GPIO.cleanup()
