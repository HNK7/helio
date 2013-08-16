#!/usr/bin/env python

import web
import sys
import socket
from brotherprint import BrotherPrint

urls = ( '/(.*)', 'api' )
app = web.application(urls, globals())

class api:
	def GET(__, name):
		if not name:
			name = 'Hello World'
		label = Label()
		label.print_singles( name )
		return name

class Label:
	def __init__(__, ip_address='192.168.0.250', mode='label' ):
		__.host = ip_address
		__.port = 9100
		__.job = None
		__.connect()
		if mode == 'line':
			__.line_initialize()
		elif mode == 'label':
			__.label_initialize()

	def connect(__):
		__.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		__.socket.connect(( __.host, __.port))
		__.job = BrotherPrint( __.socket )

	def label_initialize(__):
		__.job.initialize()
		__.job.rotated_printing('rotate')
		__.job.select_font('helsinkioutline')

	def line_initialize(__):
		__.job.initialize()
		__.job.select_font('helsinkioutline')

	def print_singles(__, name, match_id = '', division = '' ):
		match_str = match_id + ' ' + division
		__.job.feed_amount('1/8')
		__.job.char_size('33')
		__.job.send( match_str )
		__.job.line_feed()
		__.job.char_size('117')
		__.job.send( name )
		__.job.page_feed()

	def print_doubles(__, name, match_id = '', division = '' ):
		names = name.split(',')
		short_name, long_name = [names[0], names[1]] if len(names[0]) < len(names[1]) else [names[1], names[0]]
		match_str = match_id + ' ' + division
		__.job.feed_amount('1/8')
		__.job.char_size('33')
		__.job.send( match_str )
		__.job.line_feed()
		__.job.char_size('133')
		__.job.send( short_name )
		__.job.line_feed()
		__.job.send( long_name )
		__.job.page_feed()

	def print_line(__, _str, size=42 ):  # size is 33, 42, 50 ...
		__.job.feed_amount('1/8')
		__.job.char_size( str(size) )
		__.job.send( _str )
		__.job.line_feed()

	def cut(__):
		__.job.page_feed()

	def underline(__):
		__.job.char_size('33')
		__.underline = 111


if __name__ == "__main__":
	if len( sys.argv ) < 2:
		app.run()
	else:
		label = Label()
		argv = sys.argv[2:]
		if sys.argv[1] == 'singles':
			label.print_singles( *argv )
		elif sys.argv[1] == 'doubles':
			label.print_doubles( *argv )


"""

underline('off')


"""