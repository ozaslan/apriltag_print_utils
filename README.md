# AprilTag Print Utils

This repository provides python scripts for preparing PDFs ready for printing AprilTags.
The AprilTag bitmaps given at [developed site](https://april.eecs.umich.edu/software/apriltag/) are converted to larger images which are then printed into PDFs at the metric length provided by the user.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

This library is developed with Python v3.5.2 and not guaranteed to be compatiple with Python v2.x.x.
The required Python libraries are given the in following sections.

For image processing and PDF generation, this library uses ImageMagick 6.8.9-9.

```
python apriltag_print_utils.py -s 20 -t 16h5
```

### Installing

A step by step series of examples that tell you how to get a development env running


```
apt-get install imagemagick
pip3 install argparse
pip3 install glob
pip3 install pathlib
```

