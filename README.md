# Myelin-Water-Fraction
Codes related to generating myelin water fraction maps using MCDESPOT sequence
NOTE** code uses name specific commands. Please edit the code where indicated to rename folder names to better fit your project

In the code, use the 'find and replace'  tool to change the following folder names to the names of your own folders
B1MAP = B1Map_0008
DESPOT1 = SAG_DESPOT1-SEAN_0004
DESPOT2_P0 = SAG_DESPOT2_AP_P0_0005
DESPOT2_P180 = SAG_DESPOT2_AP_180_0006
MPRAGE = MPRAGE_0003

This code takes additional steps for the B1Map like dividing the intensity by 800 and taking only the last 11 images (out of 22). If you're sequence is different and you have your own B1Map already generated and properly preprocessed. UNCHECK the B1Map option while running "Convert DICOM" and 'Generate Mask" commands. RECHECK the B1Map option when running the remainder of the buttons.

//ALL OPTIONS ARE RUN FROM LEFT TO RIGHT//

STEPS FOR GENERATING MWF MAP:

Step 1. Place all raw dicom folders into a directory to be set by the 'Browse' button.

Step 2. Checkmark where you want to utilize a B1Map and Mask in the calculation process. Checkmark the MPRAGE, if you have the sequence, for white matter (WM), grey matter (GM), and whole brain (WB) segmentation results.

Step 3. Press the 'Convert DICOM' button to convert all raw DICOM folders into compressed NIFTI formart.

Step 4. Press the 'Generate Mask' button to generate a mask file from the despot 1 images.

Step 5 (optional). Before pressing the initialize button, make sure the B1Map and MPRAGE are in despot space. Resample them using an external program (3DSlicer) and name them as following: B1Map.nii.gz and MPRAGE_resample.nii.gz

Step 6. You can now go through each map generation button in the following order: T1 Map > T2 Map > MWF Map

Step 7. The Statistics button requires an MPRAGE file to segment by brain matter and provide mean statistics. Otherwise, use a statistic tool (3DSlicer) to get more in depth statistics of the generated files.

ALL NECESSARY FILES ARE PLACED IN THE ANALYSIS FOLDER



