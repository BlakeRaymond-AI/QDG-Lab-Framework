'''Defaults settings for PixeLink Camera'''

PixeLinkSettings = dict()

PixeLinkSettings['gain'] = 1.7 	# Possible Values: 0, 1.5, 3.1, 4.6	
PixeLinkSettings['expTime_ms'] = 200.0

PixeLinkSettings['useROICenter'] = False

PixeLinkSettings['ROI_left'] = 0
PixeLinkSettings['ROI_top'] = 0
PixeLinkSettings['ROI_width'] = 1280
PixeLinkSettings['ROI_height'] = 1024
PixeLinkSettings['ROI_center'] = (640, 512) # (x, y)

PixeLinkSettings['image_detail_width'] = 50
PixeLinkSettings['image_detail_height'] = 50
PixeLinkSettings['image_detail_center_x'] = 638
PixeLinkSettings['image_detail_center_y'] = 361  

PixeLinkSettings['takeData'] = False
PixeLinkSettings['processData'] = False
PixeLinkSettings['dataFolderName'] = "PixeLinkData"