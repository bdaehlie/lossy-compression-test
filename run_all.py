#!/usr/bin/python
# coding=utf8
# Written by Josh Aas
# Copyright (c) 2016, Mozilla Corporation
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the Mozilla Corporation nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os
import subprocess
import sys
import math
import shlex
import time
import glob

######## Configuration #########

# Image Type (file extension)
in_image_type = "png"

# Image Sets (names of subdirs of ./images/)
image_sets = ["kodak", "wikipedia", "tecnick"]

# Codecs
image_codecs = ["jpeg", "mozjpeg", "jxr", "webp", "hevc"]

###############################################################################

FNULL = open(os.devnull, 'w')

def print_time():
	print time.strftime('%I:%M%p %Z on %b %d, %Y')

def run_command(cmd, silent):
  if silent:
    rv = subprocess.call(cmd, stdout=FNULL, stderr=FNULL, shell=True)
  else:
    rv = subprocess.call(cmd, shell=True)
  if rv != 0:
    sys.stderr.write("Failure from subprocess:\n")
    sys.stderr.write("\t" + cmd + "\n")
    sys.stderr.write("Aborting!\n")
    sys.exit(rv)
  return rv

def main(argv):
  if len(argv) > 1:
    print "No arguments. Edit file to change configuration options."
    return

  print_time()

  for image_codec in image_codecs:
    print "Processing {0} images...".format(image_codec)
    cmd = "./rd_collect.py {0}".format(image_codec)
    for image_set in image_sets:
      cmd += " images/{0}/*.png".format(image_set)
    run_command(cmd, False)
    print "Processing {0} images complete.".format(image_codec)
    print_time()

  print "Averaging results..."
  for image_set in image_sets:
    for image_codec in image_codecs:
      wildcard_path = "images/{0}/*.{1}.out".format(image_set, image_codec)
      if len(glob.glob(wildcard_path)):
        cmd = "./rd_average.py {0} > {1}.out".format(wildcard_path, image_codec)
        run_command(cmd, False)
  print "Averaging complete."
  print_time()

  print "Creating graphs..."
  for image_set in image_sets:
    cmd = "./rd_plot.py {0}".format(image_set)
    for image_codec in image_codecs:
      cmd += " {0}.out".format(image_codec)
    run_command(cmd, False)
  print "Graphs complete."
  print_time()

if __name__ == "__main__":
  main(sys.argv)
