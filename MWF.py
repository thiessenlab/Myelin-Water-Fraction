from tkinter import filedialog
from tkinter import *
from tkinter import simpledialog
import os
import subprocess

root = Tk()

canvas = Canvas(root, width=600, height=400)
canvas.grid(columnspan=3, rowspan=5)

# Define file paths for folders
B1path = "/B1"
T1path = "/T1"
T2path = "/T2"
MWFpath = "/MWF"
MPpath = "/MPRAGE"
Analpath = "/Analysis"
Regionpath = "/Regions"


def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    os.chdir(filename)

def dicom_button():
    # Converts dicoms to NIFTI
    # Change 'SAG_DESPOT#####' to the name of your raw DICOM folders

    # DESPOT1 DICOM folder name
    os.system("dcm2niix -f \"%f_%p_%t_%s\" -m n -p y -z y \"SAG_DESPOT1-SEAN_0004\"")
    # DESPOT2 P0 DICOM folder name
    os.system("dcm2niix -f \"%f_%p_%t_%s\" -m n -p y -z y \"SAG_DESPOT2_AP_P0_0005\"")
    # DESPOT2 P180 DICOM folder name
    os.system("dcm2niix -f \"%f_%p_%t_%s\" -m n -p y -z y \"SAG_DESPOT2_AP_P180_0006\"")

    #Change folder name here aswell
    os.system("cp SAG_DESPOT1-SEAN_0004/*nii.gz DESPOT1.nii.gz")
    os.system("cp SAG_DESPOT2_AP_P0_0005/*nii.gz DESPOT2_P0.nii.gz")
    os.system("cp SAG_DESPOT2_AP_P180_0006/*nii.gz DESPOT2_P180.nii.gz")

    if var1.get() == 1:
        # Change B1MAP_0008 to the name of your raw B1MAP dicom folder
        os.system("cp -R B1MAP_0008 B1MAP;cd B1MAP;rm `ls -A | head -11`;cd ..;dcm2niix -f \"%f_%p_%t_%s\" -m n -p y -z y \"B1MAP\"")
        os.system("cp B1MAP/*nii.gz B1Map_Scan.nii.gz")

    if var3.get() == 1:
        # Change MPRAGE_0003 to the name of your raw MPRAGE dicom folder
        os.system("dcm2niix -f \"%f_%p_%t_%s\" -m n -p y -z y \"MPRAGE_0003\"")
        os.system("cp MPRAGE_0003/*nii.gz MPRAGE.nii.gz")

    print('DICOMS converted to NIFTI')


def initialize_button():
    # Sorts all the files to their respective folders and creates Mask
    # Change name of raw DICOM folder to yours
    os.makedirs('T1')
    os.makedirs('T2')
    os.makedirs('MWF')
    os.makedirs('B1')
    os.makedirs('DICOMS')
    subprocess.call(['mv', 'SAG_DESPOT1-SEAN_0004', 'DICOMS'])
    subprocess.call(['mv', 'SAG_DESPOT2_AP_P0_0005', 'DICOMS'])
    subprocess.call(['mv', 'SAG_DESPOT2_AP_P180_0006', 'DICOMS'])
    subprocess.run(['fslmerge', '-t', 'DESPOT2', 'DESPOT2_P180.nii.gz', 'DESPOT2_P0.nii.gz'])
    subprocess.call(['cp', 'DESPOT1.nii.gz', folder_path.get() + T1path])
    subprocess.call(['mv', 'DESPOT1.nii.gz', folder_path.get() + MWFpath])
    subprocess.call(['cp', 'DESPOT2.nii.gz', folder_path.get() + T2path])
    subprocess.call(['mv', 'DESPOT2_P0.nii.gz', folder_path.get() + T2path])
    subprocess.call(['mv', 'DESPOT2_P180.nii.gz', folder_path.get() + T2path])
    subprocess.call(['mv', 'DESPOT2.nii.gz', folder_path.get() + MWFpath])
    subprocess.call(['mv', 'spgr', folder_path.get() + T1path])
    subprocess.call(['mv', 'ssfp', folder_path.get() + T2path])
    subprocess.call(['mv', 'input', folder_path.get() + MWFpath])
    os.system("mv B1Map_Before.nii.gz B1Map_Scan.nii.gz DESPOT1_Volume1.nii.gz DESPOT1_Volume1_brain.nii.gz -t B1")

    if var2.get() == 1:
        subprocess.call(['cp', 'Mask.nii.gz', folder_path.get() + T1path])
        subprocess.call(['cp', 'Mask.nii.gz', folder_path.get() + T2path])
        subprocess.call(['mv', 'Mask.nii.gz', folder_path.get() + MWFpath])
    if var1.get() == 1:
        subprocess.call(['cp', 'B1Map.nii.gz', folder_path.get() + T1path])
        subprocess.call(['cp', 'B1Map.nii.gz', folder_path.get() + T2path])
        subprocess.call(['mv', 'B1Map.nii.gz', folder_path.get() + MWFpath])
        subprocess.call(['mv', 'B1MAP', 'DICOMS'])
        subprocess.call(['mv', 'B1MAP_0008', 'DICOMS'])
    if var3.get() == 1:
        os.makedirs('MPRAGE')
        os.makedirs('Analysis')
        subprocess.call(['mv', 'MPRAGE.nii.gz', folder_path.get() + MPpath])
        subprocess.call(['mv', 'MPRAGE_resample.nii.gz', folder_path.get() + MPpath])
        subprocess.call(['mv', 'MPRAGE_0003', 'DICOMS'])

    print('Initialization Done')


def create_mask():
    # Isolates one volume of despot to skull strip and generate a mask
    subprocess.call(['fslsplit', 'DESPOT1.nii.gz'])
    subprocess.call(['rm', 'vol0001.nii.gz', 'vol0002.nii.gz', 'vol0003.nii.gz', 'vol0004.nii.gz', 'vol0005.nii.gz',
                     'vol0006.nii.gz', 'vol0007.nii.gz'])
    subprocess.call(['mv', 'vol0000.nii.gz', 'DESPOT1_Volume1.nii.gz'])
    if var2.get() == 1:
        subprocess.run(['bet', 'DESPOT1_Volume1.nii.gz', 'DESPOT1_Volume1_brain.nii.gz', '-R', '-m'])
        subprocess.call(['mv', 'DESPOT1_Volume1_brain_mask.nii.gz', 'Mask.nii.gz'])
    if var1.get() == 1:
        subprocess.run(['fslmaths', 'B1Map_Scan.nii.gz', '-div', '800', 'B1Map_Before.nii.gz'])
    print('Mask Generated')


def despot1_button():
    # T1 map command
    os.chdir(folder_path.get() + T1path)
    if var1.get() == 1 and var2.get() == 1:
        os.system("qidespot1 DESPOT1.nii.gz --mask=Mask.nii.gz --B1=B1Map.nii.gz < spgr --algo=n")
    if var1.get() == 0 and var2.get() == 1:
        os.system("qidespot1 DESPOT1.nii.gz --mask=Mask.nii.gz < spgr --algo=n")
    if var1.get() == 1 and var2.get() == 0:
        os.system("qidespot1 DESPOT1.nii.gz --B1=B1Map.nii.gz < spgr --algo=n")
    if var1.get() == 0 and var2.get() == 0:
        os.system("qidespot1 DESPOT1.nii.gz < spgr --algo=n")
    os.makedirs('Output')
    subprocess.call(['cp', 'D1_T1.nii.gz', folder_path.get() + T2path + "/T1_Map.nii.gz"])
    if var3.get() == 1:
        subprocess.call(['cp', 'D1_T1.nii.gz', folder_path.get() + Analpath + "/T1_Map.nii.gz"])
    os.system("mv D1_* Output")
    print('T1 Map Generated')


def despot2_button():
    # T2 map command
    os.chdir(folder_path.get() + T2path)
    if var1.get() == 1 and var2.get() == 1:
        os.system("qidespot2fm T1_Map.nii.gz DESPOT2.nii.gz --mask=Mask.nii.gz --B1=B1Map.nii.gz < ssfp")
    if var1.get() == 0 and var2.get() == 1:
        os.system("qidespot2fm T1_Map.nii.gz DESPOT2.nii.gz --mask=Mask.nii.gz < ssfp")
    if var1.get() == 1 and var2.get() == 0:
        os.system("qidespot2fm T1_Map.nii.gz DESPOT2.nii.gz --B1=B1Map.nii.gz < ssfp")
    if var1.get() == 0 and var2.get() == 0:
        os.system("qidespot2fm T1_Map.nii.gz DESPOT2.nii.gz < ssfp")
    subprocess.call(['cp', 'FM_f0.nii.gz', folder_path.get() + MWFpath])
    if var3.get() == 1:
        subprocess.call(['cp', 'FM_T2.nii.gz', folder_path.get() + Analpath + "/T2_Map.nii.gz"])
    os.makedirs('Output')
    os.system("mv FM_* Output")
    print('T2 Map Generated')


def mwf_button():
    # MWF map command
    os.chdir(folder_path.get() + MWFpath)
    if var1.get() == 1 and var2.get() == 1:
        os.system(
            "qimcdespot DESPOT1.nii.gz DESPOT2.nii.gz --mask=Mask.nii.gz --B1=B1Map.nii.gz --f0=FM_f0.nii.gz --scale "
            "--algo=G --tesla=3 --its=4 --model=3 < input")
    if var1.get() == 0 and var2.get() == 1:
        os.system(
            "qimcdespot DESPOT1.nii.gz DESPOT2.nii.gz --mask=Mask.nii.gz --f0=FM_f0.nii.gz --scale "
            "--algo=G --tesla=3 --its=4 --model=3 < input")
    if var1.get() == 1 and var2.get() == 0:
        os.system(
            "qimcdespot DESPOT1.nii.gz DESPOT2.nii.gz --B1=B1Map.nii.gz --f0=FM_f0.nii.gz --scale "
            "--algo=G --tesla=3 --its=4 --model=3 < input")
    if var1.get() == 0 and var2.get() == 0:
        os.system("qimcdespot DESPOT1.nii.gz DESPOT2.nii.gz --f0=FM_f0.nii.gz --scale "
                  "--algo=G --tesla=3 --its=4 --model=3 < input")
    if var3.get() == 1:
        subprocess.call(['cp', '3C_f_m.nii.gz', folder_path.get() + Analpath + "/MWF_Map.nii.gz"])
    os.makedirs('Output')
    os.system("mv 3C_* Output")
    print('MWF Map Generated')


def stats_button():
    # uses MPRAGE file to generate WM, GM, and WB masks which then get applied to all maps for mean stats
    if var3.get() == 0:
        print("MPRAGE not checked")

    if var3.get() == 1:
        os.chdir(folder_path.get() + MPpath)
        subprocess.run(['bet', 'MPRAGE_resample.nii.gz', 'MPRAGE_resample_brain.nii.gz', '-R', '-m'])
        os.system("fast -t 1 -n 3 -H 0.1 -I 4 -l 20.0 -g --nopve -o MPRAGE_resample_brain MPRAGE_resample_brain")
        subprocess.call(['cp', 'MPRAGE_resample_brain_mask.nii.gz', folder_path.get() + Analpath + "/WB_Mask.nii.gz"])
        subprocess.call(['cp', 'MPRAGE_resample_brain_seg_0.nii.gz', folder_path.get() + Analpath + "/CSF_Mask.nii.gz"])
        subprocess.call(['cp', 'MPRAGE_resample_brain_seg_1.nii.gz', folder_path.get() + Analpath + "/GM_Mask.nii.gz"])
        subprocess.call(['cp', 'MPRAGE_resample_brain_seg_2.nii.gz', folder_path.get() + Analpath + "/WM_Mask.nii.gz"])
        print("Masks generated, proceeding with calculating statistics")
        os.chdir(folder_path.get() + Analpath)
        os.system("fslmaths T1_Map.nii.gz -uthr 15 T1_Map.nii.gz")
        os.system("fslmaths T2_Map.nii.gz -uthr 10 T2_Map.nii.gz")
        os.system("fslmaths MWF_Map.nii.gz -uthr 1 MWF_Map.nii.gz")
        os.system(
            "fslmaths T1_Map.nii.gz -mul CSF_Mask.nii.gz T1_Map_CSF.nii.gz; fslmaths T1_Map.nii.gz -mul "
            "WB_Mask.nii.gz T1_Map_WB.nii.gz; fslmaths T1_Map.nii.gz -mul GM_Mask.nii.gz T1_Map_GM.nii.gz; fslmaths "
            "T1_Map.nii.gz -mul WM_Mask.nii.gz T1_Map_WM.nii.gz;")
        os.system(
            "fslmaths T2_Map.nii.gz -mul CSF_Mask.nii.gz T2_Map_CSF.nii.gz; fslmaths T2_Map.nii.gz -mul "
            "WB_Mask.nii.gz T2_Map_WB.nii.gz; fslmaths T2_Map.nii.gz -mul GM_Mask.nii.gz T2_Map_GM.nii.gz; fslmaths "
            "T2_Map.nii.gz -mul WM_Mask.nii.gz T2_Map_WM.nii.gz;")
        os.system(
            "fslmaths MWF_Map.nii.gz -mul CSF_Mask.nii.gz MWF_Map_CSF.nii.gz; fslmaths MWF_Map.nii.gz -mul "
            "WB_Mask.nii.gz MWF_Map_WB.nii.gz; fslmaths MWF_Map.nii.gz -mul GM_Mask.nii.gz MWF_Map_GM.nii.gz; "
            "fslmaths MWF_Map.nii.gz -mul WM_Mask.nii.gz MWF_Map_WM.nii.gz;")
        print("-----T1 Map Statistics (WM/GM/WB) Mean values and standard deviation-----")
        os.system("fslstats T1_Map_WM.nii.gz -M -S; fslstats T1_Map_GM.nii.gz -M -S; fslstats T1_Map_WB.nii.gz -M -S")
        print("-----T2 Map Statistics (WM/GM/WB) Mean values and standard deviation-----")
        os.system("fslstats T2_Map_WM.nii.gz -M -S; fslstats T2_Map_GM.nii.gz -M -S; fslstats T2_Map_WB.nii.gz -M -S")
        print("-----MWF Map Statistics (WM/GM/WB) Mean values and standard deviation-----")
        os.system(
            "fslstats MWF_Map_WM.nii.gz -M -S; fslstats MWF_Map_GM.nii.gz -M -S; fslstats MWF_Map_WB.nii.gz -M -S")


def stats_print():
    # Only stats, if WM, GM, WB masks already exist
    os.chdir(folder_path.get() + Analpath)
    print("-----T1 Map Statistics (WM/GM/WB) Mean values and standard deviation-----")
    os.system("fslstats T1_Map_WM.nii.gz -M -S -V; fslstats T1_Map_GM.nii.gz -M -S -V; fslstats T1_Map_WB.nii.gz -M -S -V")
    print("-----T2 Map Statistics (WM/GM/WB) Mean values and standard deviation-----")
    os.system("fslstats T2_Map_WM.nii.gz -M -S -V; fslstats T2_Map_GM.nii.gz -M -S -V; fslstats T2_Map_WB.nii.gz -M -S -V")
    print("-----MWF Map Statistics (WM/GM/WB) Mean values and standard deviation-----")
    os.system(
        "fslstats MWF_Map_WM.nii.gz -M -S -V; fslstats MWF_Map_GM.nii.gz -M -S -V; fslstats MWF_Map_WB.nii.gz -M -S -V")

def lobes_input():
    # Parcelation of lobes, requires freesurfer autosegmentation to be done prior to running
    os.chdir(folder_path.get() + Analpath + Regionpath)
    pat = simpledialog.askstring("input string", "Enter Patient Freesurfer Folder Name")
    os.system("mri_annotation2label --subject " + pat + " --hemi lh --lobesStrict lobes")
    os.system("mri_annotation2label --subject " + pat + " --hemi rh --lobesStrict lobes")
    os.system("mri_aparc2aseg --s " + pat + " --labelwm --hypo-as-wm --rip-unknown --volmask --o wmparc.lobes.mgz --ctxseg aparc+aseg.mgz --annot lobes --base-offset 200")
    print("----------" + pat + " lobes segmented------------")


#GUI button parameters

browse = Button(text="Browse", command=browse_button, font='Raleway', bg="#20bebe", fg="white", height=3, width=15)
browse.grid(row=0, column=0)

folder_path = StringVar()
lbl1 = Label(master=root, textvariable=folder_path)
lbl1.grid(row=0, column=1, columnspan=2, sticky=W)

dicom = Button(text="Convert DICOM", command=dicom_button, font='Raleway', bg="#20bebe", fg="white", height=3, width=15)
dicom.grid(row=2, column=0)

mask = Button(text="Generate Mask", command=create_mask, font='Raleway', bg="#20bebe", fg="white", height=3, width=15)
mask.grid(row=2, column=1)

initialize = Button(text="Initialize", command=initialize_button, font='Raleway', bg="#20bebe", fg="white", height=3,
                    width=15)
initialize.grid(row=2, column=2)

t1map = Button(text="T1 Map", command=despot1_button, font='Raleway', bg="#20bebe", fg="white", height=3, width=15)
t1map.grid(row=3, column=0)

t2map = Button(text="T2 Map", command=despot2_button, font='Raleway', bg="#20bebe", fg="white", height=3, width=15)
t2map.grid(row=3, column=1)

mwf = Button(text="MWF Map", command=mwf_button, font='Raleway', bg="#20bebe", fg="white", height=3, width=15)
mwf.grid(row=3, column=2)

stats = Button(text="Statistics", command=stats_button, font='Raleway', bg="#20bebe", fg="white", height=3, width=15)
stats.grid(row=4, column=0)

reprint = Button(text="Reprint Statistics", command=stats_print, font='Raleway', bg="#20bebe", fg="white", height=3,
                 width=15)
reprint.grid(row=4, column=1)

lobes = Button(text="Lobes Seg", command=lobes_input, font='Raleway', bg="#20bebe", fg="white", height=3,
                 width=15)
lobes.grid(row=4, column=2)


# check box
var1 = IntVar()
b1check = Checkbutton(root, text="B1 Map", variable=var1, font='Raleway', height=3, width=15)
b1check.grid(row=1, column=0)

var2 = IntVar()
maskcheck = Checkbutton(root, text="Mask", variable=var2, font='Raleway', height=3, width=15)
maskcheck.grid(row=1, column=1)

var3 = IntVar()
mpragecheck = Checkbutton(root, text="MPRAGE", variable=var3, font='Raleway', height=3, width=15)
mpragecheck.grid(row=1, column=2)

mainloop()
