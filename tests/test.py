import asyncio
import time

async def async_foo():
    print("async_foo started")
    await asyncio.sleep(1)
    print("async_foo done")


async def main():
    asyncio.create_task(async_foo())  # fire and forget async_foo()

    # btw, you can also create tasks inside non-async funcs

    print('Do some actions 1')
    await asyncio.sleep(1)
    print('Do some actions 2')
    await asyncio.sleep(1)
    print('Do some actions 3')

def sleeeeep():
  time.sleep(1)
  print("here")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(sleeeeep())
    print("here")
    loop.run_forever()