from threading import Thread
import cv, cv2
from numpy import asarray
from numpy.linalg import eig as eigenvec

class FaceRecognizer:

	def __init__(self, inqueue, outqueue):
		self.inq = inqueue
		self.outq= outqueue

	def start_thread(self):
		'''Waits for an image to be placed in inq and returns then tries to recognize faces
		Kill the thread by placing None in the queue'''
		t = Thread(target=self.analyse_picture, name="FaceRecognizer Thread")
		t.start()



	def analyse_picture(self):
		while True:
			img = self.inq.get(block=True)				## Block on inq until StillStarter
														## sends an image
			if img == None:
				cv2.destroyAllWindows()					## Close down if it sends None
				break

			mat_img = cv.fromarray(img)
														## Initialize Storage and find faces
			storage = cv.CreateMemStorage()				## using haars.
			cascade = cv.Load("./../haar/haarcascade_frontalface_alt.xml")
			detected = cv.HaarDetectObjects(mat_img, cascade,
				 storage, 1.2, 2,cv.CV_HAAR_DO_CANNY_PRUNING, (100,100))
			if detected:
				for face in detected:					## Put each face detected in outq
					cropped_image = cv.GetSubRect(mat_img,face[0])
					self.outq.put(cropped_image)
					#uncomment for green box
					#cv.Rectangle(mat_img,p1,p2, cv.Scalar(0,255,0,0))

					## Replace this line with something other than sums if you're interested.
					## print sum(sum(sum(asarray(cropped_image))))
