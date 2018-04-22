import shelve
import socket
import random
from collections import deque

def run():

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('', 5555))
	sock.listen(10)

	while(True):
		conn, addr = sock.accept()
		print ('Connected')
		data = conn.recv(1024)
		data = data.split(' ')

		if(data[0] == 'ADD'):
			str_id = id_generator()
			data.append(str_id)
			db = shelve.open("Tasks")
			db[data[1]] = [ data[2:] ]
			print(db.values())
			db.close()
			conn.send(str_id)

		if(data[0] =='IN'):
			db = shelve.open("Tasks")
			if(db.has_key(data[1])):
				conn.send('YES')
			else:
				conn.send('NO')
			db.close()

		if(data[0] =='GET'):
			db = shelve.open("Tasks")
			return_string = db[data[1]][0][-1] + ' ' + db[data[1]][0][0] + ' ' + db[data[1]][0][1]
			conn.send(return_string)
			db.close()

		if(data[0] =='ACK'):
			db = shelve.open("Tasks")
			if(db.has_key(data[1]) and db[data[1]][0][-1] == data[2]):
				conn.send("YES")
				del db[data[1]]
			else:
				conn.send("NO")
			db.close()

		conn.close()
	sock.close()


def id_generator():
	str_id = '123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
	ls = list(str_id)
	random.shuffle(ls)
	str_id = ''.join([random.choice(ls) for x in range(10)])
	return str_id


if __name__ == '__main__':
    run()