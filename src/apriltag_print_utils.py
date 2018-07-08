#!/usr/bin/python

import os
import sys
import glob
import subprocess
from pathlib import Path
import argparse
import re

# Use argparse library for user input
parser = argparse.ArgumentParser(description='Converts an AprilTag bitmap into a PDF file ready-to-print.')
 
parser.add_argument('-s', '--tag_size'  , default = 16 , type = int, help = 'Edge length of the black tag border (cm)')
parser.add_argument('-o', '--output'    , default = '.', help = 'Output directory where the PDF files will be stored')
parser.add_argument('-p', '--parents'   , action  = 'store_true', help = 'No error if existing, make parent directories as needed')
parser.add_argument('-t', '--tag_family', default = '36h11'     , help = 'Tag family to be processed')

# Command line arguments are stores in <args>
args = vars(parser.parse_args())

# ------------------------------------------------------------------------------------------ #

# Dots-per-inches
_dpi = 150

_cwd             = os.getcwd()
_mypath          = os.path.realpath(__file__)
_bitmaps_dirname = os.path.realpath(_mypath + '/../../tag_bitmaps')

# for d in sorted(glob.glob(_bitmaps_dirname + '/tag*/')):
#  _available_tag_families.append(Path(d).parts[-1][3:])

# print('_mypath : ' + _mypath)
# print('_bitmaps_dirname : ' + _bitmaps_dirname)
# print('_available_tag_families : ' + ', '.join(_available_tag_families))

def _tagdata2Path(tag_family, tag_no):

  return glob.glob(_bitmaps_dirname + '/tag' + tag_family + '/*' + str(tag_no).zfill(5) + '.png')[0]

  # return _bitmaps_dirname + '/tag' + tag_family + '/' + str(tag_no).zfill(5) + '.png'  

def resizeTag(filepath, output_dirpath = '.'):

  tag_size = args['tag_size']

  dirname  = os.path.dirname(filepath)
  basename = os.path.splitext(os.path.basename(filepath))[0]

  if os.path.isabs(output_dirpath) == True:
    pass
  else:
    output_dirpath = os.path.realpath(_cwd + '/' + output_dirpath)

  if os.path.isdir(output_dirpath) == False:
    if args['parents'] == True:
      os.system('mkdir -p ' + output_dirpath)
    else :
      raise FileNotFoundError('Directory <' + output_dirpath + '> does not exists')

  # print('dirname : ' + dirname)
  # print('basename : ' + basename)

  # print('Filepath : %s' % filepath)
  # print('Filename base : %s' % filepath_base)

  #pxl, the size of the image with white borders
  image_size= tag_size / 0.8 / 2.54 * _dpi

  # sources : 
  # - https://unix.stackexchange.com/a/20057
  # - https://stackoverflow.com/a/48966879/6811631
  command = ['convert',
              filepath, 
             '-gravity center',
             '-density {}x{} -units PixelsPerInch'.format(_dpi, _dpi),
             '-compress jpeg -quality 70',
             '-filter Point',
             '-resize  {}x{}'.format(image_size, image_size),
             '-gravity South',
             '-font helvetica -fill LightGray -pointsize 15',
             '-draw "text 0,0 \'{}\'"'.format(basename),
             '{}/temp_{}.png'.format(dirname, basename)]

  command = ' '.join(command)
  os.system(command)

  output_filepath = '{}/{}_{}cm.pdf'.format(output_dirpath, basename, tag_size)

  command = ['convert',
             '{}/temp_{}.png'.format(dirname, basename), 
             '-gravity center',
             '-density {}x{} -units PixelsPerInch'.format(_dpi, _dpi),
             '-repage 8x11in\!',
             output_filepath]

  command = ' '.join(command)
  os.system(command)

  os.system('rm {}/temp_{}.png'.format(dirname, basename))

  '''
  command = ['evince {}/{}.pdf'.format(dirname, basename), 
             'eog {}/temp_{}.png'.format(dirname, basename)]

  for c in command:
      os.system(c + '&')
  '''

  return output_filepath

def resizeTagFamily(tag_family, output_dirpath = '.'):

  output_filepaths = []

  tagfamily_dirname = _bitmaps_dirname + '/tag' + tag_family

  for f in sorted(os.listdir(tagfamily_dirname)):
    if re.search('[0-9]{5}.png$', f):
        print('Processing : ' + f)
        output_filepaths.append(resizeTag(tagfamily_dirname + '/' + f, output_dirpath))

  # for f in  sorted(glob.glob(_bitmaps_dirname + '/tag' + tag_family + '/*.png')):
    
  return output_filepaths    

# ----------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------- #

output_filepaths = resizeTagFamily(args['tag_family'], args['output'])

print('Results are written to : ' + os.path.realpath(args['output']))