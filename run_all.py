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

######## Configuration #########

# Image Type (file extension)
in_image_type = "png"

# Image Sets (names of subdirs of ./images/)
image_sets = ["kodak", "wikipedia", "tecnick"]

# Codecs
image_codecs = ["jpeg", "mozjpeg", "jxr", "webp", "hevc"]

###############################################################################

def print_progress(iteration, total, prefix = '', suffix = '', decimals = 2, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    filledLength    = int(round(barLength * iteration / float(total)))
    percents        = round(100.00 * (iteration / float(total)), decimals)
    bar             = '█' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')
        sys.stdout.flush()

FNULL = open(os.devnull, 'w')

def shell_wildcard_matches(wildcard_path):
  test_cmd = "ls {} > /dev/null 2>&1".format(wildcard_path)
  return subprocess.call(test_cmd, stdout=FNULL, stderr=FNULL, shell=True)

def run_silent(cmd):
  rv = subprocess.call(cmd, stdout=FNULL, stderr=FNULL, shell=True)
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

  # Get list of all files we're going to operate on. We'll operate on files individually rather
  # than with shell globs so that we can show progress (this takes a while).
  image_files = ["kodak/kodim01.png"] # TODO Write code to get actual list of all files.

  #TODO Need to improve parallelization. Not efficient right now.
  print "Processing images..."
  progress_ticks_max = len(image_files) * len(image_codecs)
  progress_ticks = 0
  print_progress(progress_ticks, progress_ticks_max, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
  for image_file in image_files:
    for image_codec in image_codecs:
      cmd = "./rd_collect.py {0} images/{1}".format(image_codec, image_file)
      run_silent(cmd)
      progress_ticks += 1
      print_progress(progress_ticks, progress_ticks_max, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
  print "Image processing complete."

  print "Averaging results..."
  for image_set in image_sets:
    for image_codec in image_codecs:
      wildcard_path = "images/{0}/*.{1}.out".format(image_set, image_codec)
      if shell_wildcard_matches(wildcard_path):
        cmd = "./rd_average.py {1} > {2}.out".format(wildcard_path, image_codec)
        run_silent(cmd)
  print "Averaging complete."

  print "Creating graphs..."
  for image_set in image_sets:
    cmd = "./rd_plot.py {0}".format(image_set)
    for image_codec in image_codecs:
      cmd += " {0}.out".format(image_codec)
    run_silent(cmd)
  print "Graphs complete."

if __name__ == "__main__":
  main(sys.argv)
