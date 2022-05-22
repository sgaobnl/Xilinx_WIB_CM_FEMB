import pickle
import matplotlib.pyplot as plt
import numpy as np
import h5py
import os.path
import datetime

def ana_data(ch_data, ch_str):
    rms_f=0
    rms_t=0

    plsn = len(ch_data)//500-10
    if plsn>100:
        plsn=100

#    xlo=0
#    xhi=500
#    x=range(xlo,xhi)
#    for i in range(0,plsn):
#        plt.plot(x, ch_data[xlo+500*i:xhi+500*i])
#    plt.show()
#

    for i in range(15):
        if i == 0:
           avg_wf = ch_data[0:500]&0xffff
        else:
           avg_wf = avg_wf + ch_data[500*i:500*i+500]&0xffff
    avg_wf = avg_wf//plsn
    posp = np.where(avg_wf == np.max(avg_wf))[0][0]

    ch_data=ch_data[posp+500-50:]

    ped=[]
    for i in range(plsn):
        ped = np.concatenate((ped,ch_data[150+500*i:500+500*i]))

    rms = np.std(ped)
    return rms



fbno=227

fbno=input("FEMB board number:  ")
env="LN"
toyTPC="150pF"

rms_CHK=[]

y_hi=0
y_lo=10
name_CHK=[]


#### after boxes installed
for i in range(10):   # files for a same board
    if i==0:
        hdf_dir = "D:/IO_1826_1B/CHKOUT/FEMB{}_{}_{}/".format(fbno,env,toyTPC)
    else:
        hdf_dir = "D:/IO_1826_1B/CHKOUT/FEMB{}_{}_{}_R{:03d}/".format(fbno,env,toyTPC,i)

    fh5 = hdf_dir+"rawdata.h5"
    fb = hdf_dir+"result.bin"

    if (not os.path.exists(fh5)) or (not os.path.exists(fb)):
        continue

    with open(fb, 'rb') as fb:
         logs = pickle.load(fb)

    boxtest = datetime.datetime(2022, 5, 17, 16, 00, 00)
    if boxtest>logs["datetime"]:
        continue

    print("Open {}".format(fh5))
    good_file=True

    fp = h5py.File(fh5, 'r')
    rms_file=[]
    for j in range(128):
        CH_str = "CH{}".format(j)
        if CH_str not in fp.keys():
            good_file=False
            break

        a_rms = ana_data(fp[CH_str][()], CH_str)
        rms_file.append(a_rms)

    if not good_file:
        continue
    rms_CHK.append(rms_file)
    name_CHK.append(i)
    tmp_y_hi=np.max(np.array(rms_file))
    tmp_y_lo=np.min(np.array(rms_file))

    if tmp_y_hi>y_hi:
        y_hi=tmp_y_hi

    if tmp_y_lo<y_lo:
        y_lo=tmp_y_lo


rms_QC=[]
name_QC=[]
#### before boxes installed
for i in range(10):   # files for a same board
    if i==0:
        hdf_dir = "D:/IO_1826_1B/QC/FEMB{}_{}_{}/RMS/".format(fbno,env,toyTPC)
    else:
        hdf_dir = "D:/IO_1826_1B/QC/FEMB{}_{}_{}_R{:03d}/RMS/".format(fbno,env,toyTPC,i)

    fh5 = hdf_dir+"RMS_900mVBL_14_0mVfC_2_0us.h5"

    if not os.path.exists(fh5):
        continue

    print("Open {}".format(fh5))
    good_file=True

    fp = h5py.File(fh5, 'r')
    rms_file=[]
    for j in range(128):
        CH_str = "CH{}".format(j)
        if CH_str not in fp.keys():
            good_file=False
            break

        a_rms = ana_data(fp[CH_str][()], CH_str)
        rms_file.append(a_rms)

    if not good_file:
        continue
    rms_QC.append(rms_file)
    name_QC.append(i)
    tmp_y_hi=np.max(np.array(rms_file))
    tmp_y_lo=np.min(np.array(rms_file))

    if tmp_y_hi>y_hi:
        y_hi=tmp_y_hi

    if tmp_y_lo<y_lo:
        y_lo=tmp_y_lo
    
if y_hi+0.5>7:
    y_hi=7

save_dir = "D:/IO_1826_1B/CHKOUT/ALLCHK/"

if not (os.path.exists(save_dir)):
    try:
        os.makedirs(save_dir)
    except OSError:
        print ("Error to create folder %s"%save_dir)
        input ("hit any button and then 'Enter' to exit")
        sys.exit()    

fig,axes=plt.subplots()
x= range(128)
for i in range(len(rms_QC)):
    axes.plot(x,rms_QC[i],marker=".",label="QC R{:03d}".format(name_QC[i]))
    axes.set_ylim(y_lo-0.5,y_hi+0.5)

for i in range(len(rms_CHK)):
    axes.plot(x,rms_CHK[i],marker=".",label="CHK R{:03d}".format(name_CHK[i]))
    axes.set_ylim(y_lo-0.5,y_hi+0.5)

axes.legend()
axes.set_title("#{} Noise RMS".format(fbno))
plt.xlabel("chan")
plt.axhline(y = 2.5, color = 'r', linestyle = 'dashed')
plt.savefig(save_dir+"FEMB{}_{}_{}_RMS.png".format(fbno,env,toyTPC))
plt.show()


 
