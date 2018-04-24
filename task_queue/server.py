import shelve
import socket
import random
from collections import defaultdict
from collections import OrderedDict

def run():

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('', 5555))
	sock.listen(10)

	SP = 0
	SP_dict = defaultdict(int)

	while(True):
		conn, addr = sock.accept()
		print ('Connected')
		data = conn.recv(1024)
		data = data.split(' ')

		if(data[0] == 'ADD'):
			str_id = id_generator()
			data.append(SP)
			data.append(str_id)
			db = shelve.open("Tasks")
			db[str_id] = data[1:]
			conn.send(str_id)
			SP += 1
			db.close()

		if(data[0] =='IN'):
			db = shelve.open("Tasks")
			if ( db.has_key(data[2]) and db[data[2]][0] == data[1]):
				conn.send('YES')
			else:
				conn.send('NO')
			db.close()

		if(data[0] == 'GET'):
			db = shelve.open("Tasks")
			check_que_list = []
			for task_id in db:
				if (db[task_id][0] == data[1]):
					check_que_list.append(db[task_id])
			if (len(check_que_list) == 0):
				conn.send('NONE')
			else:
				sorted_check_que_list = sorted(check_que_list, key=lambda x : x[3] )
				return_string = sorted_check_que_list[SP_dict[data[1]]][4] + ' ' + sorted_check_que_list[SP_dict[data[1]]][1] + ' ' + sorted_check_que_list[SP_dict[data[1]]][2]
				SP_dict[data[1]] += 1
				conn.send(return_string)

		if(data[0] =='ACK'):
			db = shelve.open("Tasks")
			if(db.has_key(data[2]) and db[data[2]][0] == data[1]):
				conn.send("YES")
				db.pop(data[2])
			else:
				conn.send("NO")
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