import shelve
import socket
import random
import time


def run():

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('', 5555))
	sock.listen(10)

	timer_dict = {}
	delete = 0

	while True:
		conn, addr = sock.accept()
		data = conn.recv(1024)
		data = data.split(' ')

		#Timeout block
		for times in timer_dict:
			if(time.time() - timer_dict[times] > 300):
				print("Timeout")
				db = shelve.open("Tasks")
				#Deleting 'metka' from  task.
				#The task will be returned to the queue(with the same priority)
				db[times] = db[times][0:-1]
				delete = times
				db.close()
		if (delete):
			timer_dict.pop(delete)
			delete = 0

		if(data[0] == 'ADD'):
			db = shelve.open("Tasks")
			pointer = 0 #pointer is the priority of the queue
			#If there are already tasks in the queue, 
			#we need to determine the priority of the last one 
			if db.keys():
				for max_pointer in db.values():
					if pointer < max_pointer[3] :
						pointer = max_pointer[3]
				pointer += 1
			# Shelve data structure: "id" = [queue, length, data, pointer]
			data += [pointer]
			str_id = id_generator()
			db[str_id] = data[1:]
			conn.send(str_id)
			db.close()

		if(data[0] =='IN'):
			db = shelve.open("Tasks")
			#Check if task id is in the db
			#Then check task's queue
			if db.has_key(data[2]) and data[1] == db[data[2]][0]:
				conn.send('YES')
			else:
				conn.send('NO')
			db.close()

		if(data[0] == 'GET'):
			db = shelve.open("Tasks")
			check_que_dict = {} # key - task pointer : value - task id 
			for task_id in db:
				if (db[task_id][0] == data[1] and db[task_id][-1] != 'metka'):
					check_que_dict[ db[task_id][-1] ] = task_id
			if not len(check_que_dict):
				conn.send('NONE')
			else:
				#Find the next task to send by highest priotiry
				min_sp = min(check_que_dict.keys())
				min_id = check_que_dict[min_sp]
				return_string = min_id + ' ' + db[min_id][1] + ' ' + db[min_id][2]

				#'metka' marks the tasks as transmitted 
				# but not done yet(can return to queue later)
				# Shelve data structure: "id" = [queue, length, data, pointer, metka]
				db[min_id] += ['metka']
				conn.send(return_string)

				#Set 5 min timer for transmitted task
				#The task returns to queue if timeout('metka' will bi deleted) 
				timer_dict[min_id] = time.time()
			db.close()

		if(data[0] =='ACK'):
			db = shelve.open("Tasks")
			#if the task was transmitted and 
			if(db.has_key(data[2]) and data[1] == db[data[2]][0] and db[data[2]][-1] == 'metka'):
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
	str_id = ''.join([random.choice(ls) for x in range(10)])
	return str_id


if __name__ == '__main__':
    run()