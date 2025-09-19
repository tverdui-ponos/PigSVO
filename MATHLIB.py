import numpy as np



def length_of_vector(vector):
		
	return np.sqrt((vector[0] * vector[0]) + (vector[1] * vector[1]))


def normalize_vector( vector):
	vector = np.array(vector)
	return vector / length_of_vector(vector)
	
	
def angle_between_vectors(vector1,vector2):
	vector1 = np.array(vector1, dtype=float)
	vector2 = np.array(vector2, dtype=float)

	dx = vector2[0] - vector1[0]
	dy = vector1[1] - vector2[1]

	angle = np.arctan2(dy,dx)
	return np.degrees(angle) % 360
	

def check_angle(vector1, vector2):
	angle = angle_between_vectors(vector1, vector2)
	if 0 < angle <= 45 or 338 < angle <= 360:
		return 'right'
	elif 245 < angle <= 337:
		return 'bottom'
	elif 155 < angle <= 244:
		return 'left'
	elif 46 < angle <= 155:
		return 'top'
