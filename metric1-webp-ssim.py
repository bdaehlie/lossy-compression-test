#!/usr/bin/python
#
# Copyright 2010 Google Inc.
#
# This code is licensed under the same terms as WebM:
#  Software License Agreement:  http://www.webmproject.org/license/software/
#  Additional IP Rights Grant:  http://www.webmproject.org/license/additional/
# -----------------------------------------------------------------------------
# Modified by Josh Aas, Mozilla Corporation

import os
import sys
import time
import test_utils

def main(argv):
  png = argv[1]
  tmp_file_base = test_utils.tmpdir + os.path.basename(png)

  # JPEG quality values we're interested in.
  quality_values = [50, 55, 60, 65, 70, 75, 80, 85, 90, 95]

  # These lists will have one entry per quality value we're testing.
  jpeg_ssim_values = []
  jpeg_file_sizes = []

  # Each list will be 100 entries long, one for each quality option.
  webp_ssim_values = []
  webp_file_sizes = []

  # Calculate SSIM and file size for all JPEG quality levels.
  for q in quality_values:
    jpg = tmp_file_base + str(q) + ".jpg"
    test_utils.png_to_jpeg(png, q, jpg)
    jpeg_file_sizes.append(os.path.getsize(jpg))
    jpg_png = jpg + ".png"
    test_utils.jpeg_to_png(jpg, jpg_png)
    jpeg_ssim_values.append(test_utils.ssim_float_for_images(png, jpg_png))
    os.remove(jpg)
    os.remove(jpg_png)

  # Calculate SSIM and file size for all WebP quality levels.
  q = 0
  while q <= 100:
    webp = tmp_file_base + str(q) + ".webp"
    test_utils.png_to_webp(png, q, webp)
    webp_file_sizes.append(os.path.getsize(webp))
    webp_png = webp + ".png"
    test_utils.webp_to_png(webp, webp_png)
    webp_ssim_values.append(test_utils.ssim_float_for_images(png, webp_png))
    os.remove(webp)
    os.remove(webp_png)
    q += 1

  # For each quality value we're interested in, calculate the size of a
  # WebP file that is equivalent to the JPEG file via interpolation.
  webp_ssim_equiv_file_sizes = []
  for s in jpeg_ssim_values:
    interpolated = test_utils.lists_interpolate(webp_ssim_values, s, webp_file_sizes)
    webp_ssim_equiv_file_sizes.append(interpolated)

  jpeg_total_size = 0
  for fs in jpeg_file_sizes:
    jpeg_total_size += fs

  webp_total_size = 0
  for fs in webp_ssim_equiv_file_sizes:
    webp_total_size += fs

  print "File size change from JPEG to WebP at equivalent SSIM: " + str(float(webp_total_size) / float(jpeg_total_size))[:5]

if __name__ == "__main__":
  main(sys.argv)
