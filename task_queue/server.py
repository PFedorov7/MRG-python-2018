import shelve
import socket
import random
from collections import defaultdict
from collections import OrderedDict

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
			db = shelve.open("Tasks")
			SP = 0
			if db.keys():
				for max_sp in db.values():
					if SP < max_sp[3] :
						SP = max_sp[3]
				SP += 1
			# "id" = [queue, length, data, SP]
			data += [SP]
			str_id = id_generator()
			db[str_id] = data[1:]
			conn.send(str_id)
			db.close()

		if(data[0] =='IN'):
			db = shelve.open("Tasks")
			if db.has_key(data[2]):
				conn.send('YES')
			else:
				conn.send('NO')
			db.close()

		if(data[0] == 'GET'):
			db = shelve.open("Tasks")
			check_que_dict = {}
			for task_id in db:
				if (db[task_id][0] == data[1] and db[task_id][-1] != 'metka'):
					check_que_dict[ db[task_id][-1] ] = task_id
			if not len(check_que_dict):
				conn.send('NONE')
			else:
				min_sp = min(check_que_dict.keys())
				min_id = check_que_dict[min_sp]
				return_string = min_id + ' ' + db[min_id][1] + ' ' + db[min_id][2]
				db[min_id] += ['metka']
				conn.send(return_string)
			db.close()

		if(data[0] =='ACK'):
			db = shelve.open("Tasks")
			if(db.has_key(data[2])):
				conn.send("YES")
				db.pop(data[2])
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

def timeout():
	pass

if __name__ == '__main__':
    run()