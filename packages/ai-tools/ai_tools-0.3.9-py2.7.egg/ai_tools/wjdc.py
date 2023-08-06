import numpy
import numpy as np
import imageio
from ai_tools import video2img as vi
from vcvf_emotion import face_emotion as fe
from distutils.sysconfig import get_python_lib
from sklearn.externals import joblib
import pdb
import os
import cv2
import sys
from zprint import *
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
#fe0=fe.face_emotion()
sppath=get_python_lib()
mpath=os.path.join(sppath,"ai_tools/data/wjdc_clf_800.pkl")
print("%s exits: %s"%(mpath,os.path.exists(mpath)))
clf_wjdc=joblib.load(mpath)
def init():
    global fe0
    fe0=fe.face_emotion()
def get_imglist_face_emotion(images):
    global fe0
    smile_image=[]
    smile_score_l=[]
    top_l=[]
    left_l=[]
    size_l=[]
    c=1
    for img in images:
        #rect=[96,96,185,186]
        #print(fe0.face_emotion_rect(img,rect))
        score,rect,time_cost=fe0.face_emotion(img)
        if(len(score)==0):
            score.append(0)
        if(len(rect)==0):
            rect.append(fe0.rect_opencv2dlib([1,1,2,2]))
        sys.stdout.write("\r"+40*" ")
        sys.stdout.write("\r%5s/%5s,%5s,%15s"%(c,len(images),score,rect))
        sys.stdout.flush()
        dl=rect
        sl=score
        #pdb.set_trace()
        smile_score_l.append(sl[0])
        top_l.append(float(dl[0].top())/float(img.shape[0]))
        left_l.append(float(dl[0].left())/float(img.shape[1]))
        size_l.append(  float(float(dl[0].bottom())-float(dl[0].top()))/float(img.shape[0]))
        if(sl[0]>0.8):
            smile_image.append(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
        c=c+1
    return smile_score_l,top_l,left_l,size_l,smile_image 
def list2matrix(smile_score_l,top_l,left_l,size_l):
     #pdb.set_trace() 
     x0=np.zeros((len(top_l),4))
     x0[:,0]=np.array(smile_score_l)
     x0[:,1]=np.array(top_l)
     x0[:,2]=np.array(left_l)
     x0[:,3]=np.array(size_l)
     x1=cv2.resize(x0,(800,4),cv2.INTER_CUBIC) 
     feature=x1.reshape((1,x1.shape[0]*x1.shape[1]))
     return feature
def write2file(ffn,smile_score_l,top_l,left_l,size_l):
     #ffn="wjdcfeature_rate_1/%s_%s.wjdc.txt"%(lumi_class,infostrl[0])
     ffnh=open(ffn,'w')
     for i in range(0,len(top_l)):
         ffnh.write("%s,"%(smile_score_l[i]))
         ffnh.write("%s,"%(top_l[i]))
         ffnh.write("%s,"%(left_l[i]))
         ffnh.write("%s\n"%(size_l[i]))
     ffnh.close()
    
def get_wjdc_feature(video_url,wget_flag=1,rate=0.1):
    if(wget_flag==1):
        images=vi.flv2img_wget(video_url,rate,0,4000)
    else:
        images=vi.flv2img(video_url,rate,0,4000)
    zprint("images:%s"%(len(images)))
    sm_l,top_l,left_l,size_l,simg_l=get_imglist_face_emotion(images)
    feature=list2matrix(sm_l,top_l,left_l,size_l)
    return feature
def wjdc_classify(video_url,wget_flag=1,rate=0.1):
    global clf_wjdc 
    x=get_wjdc_feature(video_url,wget_flag,rate)
    #pdb.set_trace()
    re=wjdc_classify_from_feature(x)
    return re
def wjdc_classify_from_feature(x):
    global clf_wjdc 
    y_pred = clf_wjdc.predict_proba(x)
    zprint("y_pred=%s"%(y_pred))
    y_pred_sort_index=np.argsort(y_pred)
    y_pred_l=y_pred_sort_index[:,-1]
    #ddict=["wjdc","nwjdc"]
    ddict=["nwjdc","wjdc"]
    zprint(ddict[y_pred_l[0]])
    return ddict[y_pred_l[0]]
def work1(video_url,class_id):
    images=vi.flv2img_wget(video_url,1,0,4000)
    sm_l,top_l,left_l,size_l,simg_l=get_imglist_face_emotion(images)
    ffn="wjdcfeature_test1k/%s_%s.wjdc.txt"%("test",class_id)
    write2file(ffn,sm_l,top_l,left_l,size_l)
    
    print(ffn)
    return simg_l
if __name__=="__main__":
    
    argsl=sys.argv[1].strip("\n").split(" ")
    print(argsl)
    role=argsl[0]
    video_url=argsl[1]
    class_id=argsl[2]
    #print(get_wjdc_feature(sys.argv[1]))
    #work1(video_url,class_id)
    wjdc_classify(video_url,0)

