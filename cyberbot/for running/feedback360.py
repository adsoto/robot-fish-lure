# microbit-module: feedback360@0.8.0
"""library for parallax 360 feedback motors. Should be imported onto microbit transmitter and reciever initially"""
from cyberbot import *
class drive():
	def __init__(self,p=0):
		self.pin=p
	def connect():
		bot(18,19).send_c(61)
	def speed(l,r):
		bot(18,19).send_c(62,0,l,r)
	def goto(l,r):
		bot(18,19).send_c(63,0,l,r)
	def set_acceleration(l,r):
		bot(18,19).send_c(64,0,l,r)