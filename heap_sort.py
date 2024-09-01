import random
random.seed(0)

from contextlib import contextmanager

@contextmanager
def handle_exceptions():
	try:
		yield
	except Exception as e:
		print(e)


class Node:
	def __init__(self, val):
		self.val = val
		self.left = None
		self.right = None

class Heap:

	def __init__(self):
		self.head = None

	def insert(self, node):
		if type(node)!=Node:
			node = Node(node)

		if not self.head:
			self.head = node
			return

		cur = self.head
		before = None
		while cur:
			if node.val>cur.val:
				if not cur.left:
					cur.left = node
					return
				elif not cur.right:
					cur.right = node
					return
				else:
					before = cur
					if random.randint(0, 1):
						cur = cur.left 
					else:
						cur = cur.right
			else: # node.val<=cur.val
				if not before: 
					self.head = node # set head to node
					if random.randint(0, 1):
						node.left = cur
					else:
						node.right = cur
					return
				
				if before.left is cur:
					before.left = node
					
					cur_left = cur.left
					cur_right = cur.right

					cur.left = None
					cur.right = None

					node.left = cur_left
					node.right = cur_right

					if not node.left:
						node.left = cur
						return
					elif not node.right:
						node.right = cur
						return
					elif node.left and node.right:
						before = node
						node = cur
						if random.randint(0, 1):
							cur = cur_left # Go to left in default
						else:
							cur = cur_right
					else: 
						raise("Insert Error.")

					return
				else:
					before.right = node

					cur_left = cur.left
					cur_right = cur.right

					cur.left = None
					cur.right = None

					node.left = cur_left
					node.right = cur_right

					if not node.left:
						node.left = cur
						return
					elif not node.right:
						node.right = cur
						return
					elif node.left and node.right:
						before = node
						node = cur
						if random.randint(0, 1):
							cur = cur_left
						else:
							cur = cur_right
					else: 
						raise("Insert Error.")

					return
					return

	def unlink_node(self, parent, parent_methods):
		if parent_methods=='left':
			parent.left = None
		elif parent_methods=='right':
			parent.right = None
		else:
			raise("Unlink Error.")

	def pop_bottom(self):
		before = self.head

		if not before:
			return None
		elif not (before.left or before.right):
			self.head = None
			return before

		if before.left:
			cur = before.left
			method = 'left'
		elif before.right:
			cur = before.right
			method = 'right'

		while True:
			# print("cur:", cur.val)
			# with handle_exceptions(): print('cur.left.val:', cur.left.val)
			# with handle_exceptions(): print('cur.right.val:', cur.right.val)

			if not (cur.left or cur.right):
				self.unlink_node(before, method)
				return cur
			elif cur.left:
				before = cur
				cur = cur.left
				method = 'left'
			else:
				before = cur
				cur = cur.right
				method = 'right'
			

	def exchange_left_child(self, parent):
		cur_left = parent.left
		cur_right = parent.right

		child_left = cur_left.left
		child_right = cur_left.right

		parent.left = child_left
		parent.right = child_right

		cur_left.left = parent
		cur_left.right = cur_right

		return cur_left

	def exchange_right_child(self, parent):
		cur_left = parent.left
		cur_right = parent.right

		child_left = cur_right.left
		child_right = cur_right.right

		parent.left = child_left
		parent.right = child_right

		cur_right.left = cur_left
		cur_right.right = parent

		return cur_right

	def link_parent(self, parent, node, parent_methods):
		if parent_methods=='left':
			parent.left = node
		elif parent_methods=='right':
			parent.right = node


	def tidy_up(self, node, parent=None, parent_methods=None):
		if not node:
			return None
		elif (not node.left) and (not node.right):
			return node
		elif node.left and node.right:
			if node.left.val < node.right.val:
				if node.left.val <node.val:
					new_top = self.exchange_left_child(node)
					self.tidy_up(node, new_top, 'left')
					if parent:
						self.link_parent(parent, new_top, parent_methods)
					else:
						self.head = new_top

					return
				else:
					return

			elif node.left.val >= node.right.val:
				if node.right.val <node.val:
					new_top = self.exchange_right_child(node)
					self.tidy_up(node, new_top, 'right')
					if parent:
						self.link_parent(parent, new_top, parent_methods)
					else:
						self.head = new_top

					return
				else:
					return


		elif node.left and (not node.right):
			if node.left.val<node.val:
				new_top = self.exchange_left_child(node)
				self.tidy_up(node, new_top, 'left')
				if parent:
					self.link_parent(parent, new_top, parent_methods)
				else:
					self.head = new_top

			else:
				return

		elif (not node.left) and node.right:
			if node.right.val<node.val:
				new_top = self.exchange_right_child(node)
				self.tidy_up(node, new_top, 'right')
				if parent:
					self.link_parent(parent, new_top, parent_methods)
				else:
					self.head = new_top

			else:
				return
		
		return

	def get_min(self):
		bottom = self.pop_bottom()
		if not self.head:
			return bottom.val

		top = self.head
		top_left = top.left
		top_right = top.right

		top.left = None
		top.right = None

		self.head = bottom
		self.head.left = top_left
		self.head.right = top_right

		self.tidy_up(self.head)

		return top.val

def main():
	# list0 = [5, 6, 4, 9, 8, 4.5, 11, 25]
	list0 = [7, 11, 3, 6, 18, 29, 137, 90, 0, 1]
	heap = Heap()
	for x in list0:
		print('Insert:', x)
		heap.insert(x)


	
		# heap.head.left.val
		# heap.head.right.val
		# heap.head.left.left.val
		# heap.head.left.right.val
		# heap.head.right.left.val
		# heap.head.right.right.val
		# heap.head.left.left.left.val
		# heap.head.left.left.right.val
		# heap.head.left.right.left.val
		# heap.head.left.right.right.val
		# heap.head.right.left.left.val
		# heap.head.right.left.right.val
		# heap.head.right.right.left.val


	# with handle_exceptions(): print('heap.head.val:', heap.head.val)
	# with handle_exceptions(): print('heap.head.left.val:', heap.head.left.val)
	# with handle_exceptions(): print('heap.head.right.val:', heap.head.right.val)
	# with handle_exceptions(): print('heap.head.left.left.val:', heap.head.left.left.val)
	# with handle_exceptions(): print('heap.head.left.right.val:', heap.head.left.right.val)
	# with handle_exceptions(): print('heap.head.right.left.val:', heap.head.right.left.val)
	# with handle_exceptions(): print('heap.head.right.right.val:', heap.head.right.right.val)
	# with handle_exceptions(): print('heap.head.left.left.left.val:', heap.head.left.left.left.val)
	# with handle_exceptions(): print('heap.head.left.left.right.val:', heap.head.left.left.right.val)
	# with handle_exceptions(): print('heap.head.left.right.left.val:', heap.head.left.right.left.val)
	# with handle_exceptions(): print('heap.head.left.right.right.val:', heap.head.left.right.right.val)
	# with handle_exceptions(): print('heap.head.right.left.left.val:', heap.head.right.left.left.val)
	# with handle_exceptions(): print('heap.head.right.left.right.val:', heap.head.right.left.right.val)
	# with handle_exceptions(): print('heap.head.right.right.left.val:', heap.head.right.right.left.val)



	print('\nSorted:')
	while True:
		print(heap.get_min())
		if not heap.head:
			break

if __name__=='__main__':
	main()
	print('\nDone!\n')



