#!/usr/bin/env python3
from .build import build
import os, sys

def main():
	
	# Our supported commands
	COMMANDS = {
		'build': {
			'function': build,
			'description': 'Builds containers for a specific version of UE4'
		}
	}
	
	# Truncate argv[0] to just the command name without the full path
	sys.argv[0] = os.path.basename(sys.argv[0])
	
	# Determine if a command has been specified
	if len(sys.argv) > 1:
		
		# Verify that the specified command is valid
		command = sys.argv[1]
		if command not in COMMANDS:
			print('Error: unrecognised command "{}".'.format(command), file=sys.stderr)
			sys.exit(1)
		
		# Invoke the command
		sys.argv = [sys.argv[0]] + sys.argv[2:]
		COMMANDS[command]['function']()
		
	else:
		
		# Determine the longest command name so we can format our list in nice columns
		longestName = max([len(c) for c in COMMANDS])
		minSpaces = 6
		
		# Print usage syntax
		print('Usage: {} COMMAND [OPTIONS]\n'.format(sys.argv[0]))
		print('Windows and Linux containers for Unreal Engine 4\n')
		print('Commands:')
		for command in COMMANDS:
			whitespace = ' ' * ((longestName + minSpaces) - len(command))
			print('  {}{}{}'.format(
				command,
				whitespace,
				COMMANDS[command]['description']
			))
		print('\nRun `{} COMMAND --help` for more information on a command.'.format(sys.argv[0]))
