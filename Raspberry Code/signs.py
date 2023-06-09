# constants used throughout the code to help make sense of it later
SPEED_BUMP, CROSSING, BUMPY_ROAD, YIELD, STOP, FORBIDDEN = 0, 13, 1, 2, 3, 4
SP10, SP40, SP60, NO_ENTRY, ROUNDABOUT = 5, 6, 7, 8, 9
END_OF_AL, PRIORITY, PARKING = 10, 11, 12

# all the signs the model can detect, with names
signs = {
  0: 'Speed bump',
  1: 'Bumpy Road',
  2: 'Yield',
  3: 'STOP',
  4: 'Forbidden for everything',
  5: 'Speed limit - 10',
  6: 'Speed limit - 40',
  7: 'Speed limit - 60',
  8: 'No entry',
  9: 'Roundabout',
  10: 'End of All Restrictions',
  11: 'Priority Road',
  12: 'Parking',
  13: 'Pedestrian Crossing',}

# signs that we will ignore
# End of All Restrictions is ignored because the model tends to see it 
# where it is not
unused_signs = [10]

# all signs except the unused ones
used_signs = [key for key in signs.keys() if key not in unused_signs]

# check if a result is valid, which is decided by seeing if the sign is in the used_signs list
def is_valid(result):
  if result is None:
    return False
  return result[-1].item() in used_signs

# go from a class id to a sign name
def get_name(result):
  box, confidence, classs = result
  return signs[classs]

# the rectangular box is given by 4 coordinates, xmin, ymin, xmax and ymax
# computes the area of the bounding box using those coordinates
def get_area(result):
  box, confidence, classs = result
  xmin, ymin, xmax, ymax = box[0], box[1], box[2], box[3]
  return (xmax - xmin) * (ymax - ymin)