# from queue import Queue
#
# # Create an empty queue
# q = Queue()
# while True:
#     # Get input from the user
#     input_str = str(input("Enter a value to add to the queue: "))
#
#     # Add the input to the queue
#     q.put(input_str)
#
#     print("Prompt added to the queue:")
#     print(input_str+"\n")
#
#     while not q.empty():
#         print(q.get())

# # Attempt 2
# import threading
# from queue import Queue
# import time
#
# # Create an empty queue
# q = Queue()
#
# def add_input_to_queue():
#   while True:
#       # Get input from the user
#       input_str = input("Enter a value to add to the queue: ")
#
#       # Add the input to the queue
#       q.put(input_str)
#
#       print("Value added to the queue.")
#
# # Create a new thread
# thread = threading.Thread(target=add_input_to_queue)
#
# # Start the thread
# thread.start()
#
# def print_queue():
#     assert q, "Queue does not exist"
#     while True:
#         print(q.qsize())
#         time.sleep(2)
#
# thread2 = threading.Thread(target=print_queue)
#
# # Start the thread
# thread2.start()

import threading
import time
from queue import Queue

# Create an empty queue
q = Queue()

def add_input_to_queue():
  while True:
      # Get input from the user
      input_str = input("Enter a value to add to the queue: ")

      # Add the input to the queue
      q.put(input_str)

      print("Value added to the queue.")

def print_queue_length():
  while True:
      # Print the number of items in the queue
      print("Number of items in the queue:", q.qsize())

      # Sleep for 5 seconds
      time.sleep(5)

# Create two new threads
thread1 = threading.Thread(target=add_input_to_queue)
thread2 = threading.Thread(target=print_queue_length)

# Start the threads
thread1.start()
thread2.start()
