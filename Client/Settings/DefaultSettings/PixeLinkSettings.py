'''Default settings for PixeLink Camera'''
PixeLinkSettings = dict()
PixeLinkSettings['gain'] = 0 	# Image Gain. Possible values: 0, 1.5, 3.1, 4.6	
PixeLinkSettings['expTime_ms'] = 10.0 	# Image Exposure Time
PixeLinkSettings['ROI_width'] = 1280	
PixeLinkSettings['ROI_height'] = 1024
PixeLinkSettings['ROI_left'] = 0
PixeLinkSettings['ROI_top'] = 0
PixeLinkSettings['useROICenter'] = False	# Set region of interest based on 
								# center location and width and height settings.
PixeLinkSettings['ROI_center'] = (640, 512) # Location of center. (x, y)
PixeLinkSettings['takeData'] = False
PixeLinkSettings['processData'] = False
PixeLinkSettings['dataFolderName'] = "PixeLinkData"
