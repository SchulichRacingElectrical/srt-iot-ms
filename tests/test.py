# import asyncio
# import time

# async def async_foo():
#     print("async_foo started")
#     await asyncio.sleep(1)
#     print("async_foo done")


# async def main():
#     asyncio.create_task(async_foo())  # fire and forget async_foo()

#     # btw, you can also create tasks inside non-async funcs

#     print('Do some actions 1')
#     await asyncio.sleep(1)
#     print('Do some actions 2')
#     await asyncio.sleep(1)
#     print('Do some actions 3')



# asyncio.run_coroutine_threadsafe(main(), asyncio.get_event_loop())
# print("here")
# print("hi")

import asyncio
import threading
import time



async def another_function(i):
  print("starting sleep")
  print("stopping sleep")
  print(i)

async def read():
  loop = asyncio.new_event_loop()
  threading.Thread(target=loop.run_forever).start()
  tasks = []
  for i in range(0, 5):
    print("Starting read")
    tasks.append(asyncio.run_coroutine_threadsafe(another_function(i), loop))
    print("Ending read")
  for task in tasks:
    task.result()
    print(task._state == "FINISHED")
  loop.call_soon_threadsafe(loop.stop)

def start():
  asyncio.run(read())

def main():
  listener = threading.Thread(target=start)
  listener.start()

main()