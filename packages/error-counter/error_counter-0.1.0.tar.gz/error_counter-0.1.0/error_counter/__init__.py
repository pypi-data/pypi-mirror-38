# coding:utf-8 Copy Right Atelier Grenouille © 2018 -
#
import os
import subprocess
from incremental_counter import Counter as C

class Counter:
  def __init__(self, counterfile, reset_task="sudo reboot", reset_threshold=3):
    self.counter         = C(counterfile)
    self.reset_task      = reset_task
    self.reset_threshold = reset_threshold

  def reset_device(self):
    subprocess.Popen(self.reset_task, shell=True)

  def inc_error(self):
    if self.counter.inc() >= self.reset_threshold:
      self.reset_device()

  def dec_error(self):
    self.counter.dec()

  def reset_error(self):
    self.counter.reset()

