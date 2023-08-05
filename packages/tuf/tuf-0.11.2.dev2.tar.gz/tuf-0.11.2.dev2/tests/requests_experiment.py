import threading
import requests
import time
import timeout_decorator

l = 10*1024*1024

def reader(l):
  print('Length remaining before read: ' + str(r.raw.length_remaining))
  z = r.raw.read(l)
  print('Read ' + str(l) + ' bytes. Remaining after read: ' + str(r.raw.length_remaining))

t = threading.Thread(target=reader, args=[l])
r = requests.get('https://cdimage.debian.org/cdimage/weekly-builds/amd64/iso-cd/debian-mac-testing-amd64-netinst.iso', stream=True, timeout=2)

def status():
  print('Request open? ' + str(not r.raw.isclosed()))
  print('Thread alive? ' + str(t.is_alive()))
  print('Remaining bytes: ' + str(r.raw.length_remaining))

def status_nothread():
  print('Request open? ' + str(not r.raw.isclosed()))
  print('Remaining bytes: ' + str(r.raw.length_remaining))


def wait_on_thread_and_report():
  done = False
  t.start()
  status()
  while not done:
    print('--Waiting on thread, 3s...')
    time.sleep(3)
    status()
    done = not t.is_alive()


def stop_thread_after_a_bit():
  print('--Initial')
  status()
  print('--Starting')
  t.start()
  status()
  print('--Sleeping 3s')
  time.sleep(3)
  status()
  print('--Stopping thread')
  t._stop()
  time.sleep(0.2)
  status()


@timeout_decorator.timeout(5)
def read_w_decorator():
  reader(l)

@timeout_decorator.timeout(5, use_signals=False)
def read_w_decorator_proc():
  reader(l)


def test_decorator(signals=True):
  print('--Initial')
  status_nothread()
  print('--Starting')

  try:
    if signals:
      read_w_decorator()
    else:
      read_w_decorator_proc()
  except timeout_decorator.timeout_decorator.TimeoutError as e:
    print('\nCaught timeout. Error follows: ' + str(e))
  else:
    print('\nNO TIMEOUT CAUGHT\n')

  print('--Final')
  status_nothread()



def test_poolclose():  # DOES NOT WORK: Download continues.
  print('--Initial')
  status()
  print('--Starting')
  t.start()
  status()
  print('--Sleeping 5s')
  time.sleep(5)
  status()
  print('--Closing')
  r.raw._pool.close()
  time.sleep(0.2)
  status()
  print('--Waiting 2.5s')
  time.sleep(2.5)
  status()



def test_connclose():   # DOES NOT WORK: Download continues.
  print('--Initial')
  status()
  print('--Starting')
  t.start()
  status()
  print('--Sleeping 5s')
  time.sleep(5)
  status()
  print('--Closing')
  r.connection.close()
  time.sleep(0.2)
  status()
  print('--Waiting 2.5s')
  time.sleep(2.5)
  status()



def test_normclose(): # DOES NOT WORK: Download continues AND it downloads the whole thing. (close reads all first)
  print('--Initial')
  status()
  print('--Starting')
  t.start()
  status()
  print('--Sleeping 5s')
  time.sleep(5)
  status()
  print('--Closing')
  r.raw.close()
  time.sleep(0.2)
  status()
  print('--Waiting 2.5s')
  time.sleep(2.5)
  status()

