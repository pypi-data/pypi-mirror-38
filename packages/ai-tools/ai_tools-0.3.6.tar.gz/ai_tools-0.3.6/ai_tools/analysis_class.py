
import numpy
import numpy as np
import imageio
from ai_tools import video2img as vi
#from vcvf_emotion import face_emotion as fe
import pdb
import os
import cv2
import sys
import numpy
import imageio
from ai_tools import video2img as vi
import pdb
import os
import cv2
import sys           
from zprint import *
os.environ['CUDA_VISIBLE_DEVICES']="-1"

#fe0=fe.face_emotion()
def get_face_emotion_from_imglist(images):
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
     return x1
def write2file(ffn,smile_score_l,top_l,left_l,size_l):
     #ffn="wjdcfeature_rate_1/%s_%s.wjdc.txt"%(lumi_class,infostrl[0])
     ffnh=open(ffn,'w')
     for i in range(0,len(top_l)):
         ffnh.write("%s,"%(smile_score_l[i]))
         ffnh.write("%s,"%(top_l[i]))
         ffnh.write("%s,"%(left_l[i]))
         ffnh.write("%s\n"%(size_l[i]))
     ffnh.close()
    
def get_wjdc_feature(video_url):
    images=vi.flv2img(video_url,0.1,0,4000)
    sm_l,top_l,left_l,size_l,simg_l=get_face_emotion_from_imglist(images)
    x1=list2matrix(sm_l,top_l,left_l,size_l)
    return x1
def work1(video_url,class_id):
    images=vi.flv2img_wget(video_url,1,0,4000)
    sm_l,top_l,left_l,size_l,simg_l=get_imglist_face_emotion(images)
    ffn="wjdcfeature_test1k/%s_%s.wjdc.txt"%("test",class_id)
    write2file(ffn,sm_l,top_l,left_l,size_l)
    
    print(ffn)
    return simg_l
def demo1():    
    argsl=sys.argv[1].strip("\n").split(" ")
    print(argsl)
    role=argsl[0]
    video_url=argsl[1]
    class_id=argsl[2]
    #print(get_wjdc_feature(sys.argv[1]))
    work1(video_url,class_id)
def get_smile(images):
    images_smile=[]
    c=1
    for img in images:
        #rect=[96,96,185,186]
        #print(fe0.face_emotion_rect(img,rect))
        score,rect,time_cost=fe0.face_emotion(img)
	if(len(score)>0 and score[0]>0.8):
        	#images_smile.append(img)
        	images_smile.append(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
        	sys.stdout.write("\rlen(images),len(smile)=[%d,%d/%d],score=%s,%s"%(len(images),len(images_smile),c,score,score[0]>0.8))
        c=c+1
    return images_smile
def create_gif(gif_name,video_url):
    images=vi.flv2img(video_url,1,0,4000)
    image_smile=get_smile(images)

    dura=0.1
    #images=imageio.imiread("qq.gif")
    #imageio.mimsave("teacher.gif",list(numpy.array(images)[numpy.array(range(0,53,12))]),duration=0.00001)
    #imageio.mimsave("teacher.gif",list(numpy.array(images)[numpy.array(range(0,50,2))]),duration=0.1)
    imageio.mimsave(gif_name+"%s.gif"%(len(image_smile)*0.05),list(numpy.array(image_smile)[numpy.array(range(0,len(image_smile),2))]),duration=dura)
    print("gif duraton:%s s"%(len(image_smile)*0.1*0.5))
def create_gif_from_imglist(gif_name,images):
    #images=vi.flv2img_wget(video_url,1,0,4000)
    #image_smile=get_smile(images)
    image_smile=images

    dura=0.1
    #images=imageio.imiread("qq.gif")
    #imageio.mimsave("teacher.gif",list(numpy.array(images)[numpy.array(range(0,53,12))]),duration=0.00001)
    #imageio.mimsave("teacher.gif",list(numpy.array(images)[numpy.array(range(0,50,2))]),duration=0.1)
    imageio.mimsave(gif_name+"%s.gif"%(len(image_smile)*0.05),list(numpy.array(image_smile)[numpy.array(range(0,len(image_smile),2))]),duration=dura)
    print("gif duraton:%s s"%(len(image_smile)*0.1*0.5))
def demo2():
    base_url="/data1/mingmingzhao/data_sets/mp4/"
    video_all="vipkid_jz3bc4e1e7458f49a381297ee384773637_f_1522312337659_t_1522313938697.mp4,vipkid_jz40c0afcf42a54577ae80a668a8593600_f_1532087814504_t_1532089561969.mp4,vipkid_jz932a9ba4f1fd4fd5809b333a366dd64a_f_1530336593475_t_1530338142709.mp4,vipkid_jzbfad3425917946f0abaafaea966117a9_f_1531744118258_t_1531745977835.mp4,vipkid_jzc0fc4672202b492594b3d094b010a6e1_f_1531826923257_t_1531828692939.mp4,vipkid_jzd28621035a7c4304805b38d397d148ae_f_1530872632184_t_1530874638548.mp4"
    video_list=video_all.split(',')
    for video in video_list:
        video_url=os.path.join(base_url,video)
        gif_name=video.split("_")[1]
        #pdb.set_trace()
        create_gif(gif_name,video_url)
def analysis_teacher(teacher_url,fe1):
    zprint("downloading:%s"%(teacher_url))
    imgs=vi.flv2img_wget(teacher_url,1,0,100)
    face_num=0
    smile_num=0
    hand_num=0
    c=0
    smile_score_l=[]
    top_l=[]
    left_l=[]
    size_l=[]
    smile_image=[]
    for img in imgs:
        score,rect,time_cost=fe1.face_emotion(img)
        
        if(len(score)==0):
            score.append(0)
        else:
            face_num+=1
        if(len(rect)==0):
            rect.append(fe1.rect_opencv2dlib([1,1,2,2]))
        sys.stdout.write("\r"+40*" ")
        sys.stdout.write("\r%5s/%5s,%5s,%15s"%(c,len(imgs),score,rect))
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
            smile_num+=1
        c+=1
    info={"smile_image":smile_image,"face_num":face_num,"smile_num":smile_num,"hand_num":hand_num,"smile_score_l":smile_score_l,"top_l":top_l,"left_l":left_l,"size_l":size_l}
    #return face_num,smile_num,hand_num
    return info
def analysis_student(student_url,fe1):
    zprint("downloading:%s"%(student_url))
    imgs=vi.flv2img_wget(student_url,1,0,100)
    face_num=0
    smile_num=0
    half_face_num=0
    c=0
    smile_score_l=[]
    top_l=[]
    left_l=[]
    size_l=[]
    smile_image=[]
    for img in imgs:
        score,rect,time_cost=fe1.face_emotion(img)
        if(len(score)==0):
            score.append(0)
        else:
            face_num+=1
        if(len(rect)==0):
            rect.append(fe1.rect_opencv2dlib([1,1,2,2]))
        sys.stdout.write("\r"+40*" ")
        sys.stdout.write("\r%5s/%5s,%5s,%15s"%(c,len(imgs),score,rect))
        sys.stdout.flush()
        sl=score
        dl=rect
        smile_score_l.append(sl[0])
        top_l.append(float(dl[0].top())/float(img.shape[0]))
        left_l.append(float(dl[0].left())/float(img.shape[1]))
        size_l.append(  float(float(dl[0].bottom())-float(dl[0].top()))/float(img.shape[0]))
        if(sl[0]>0.8):
            smile_image.append(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
            smile_num+=1
        c+=1
    info={"smile_image":smile_image,"face_num":face_num,"smile_num":smile_num,"half_face_num":half_face_num,"smile_score_l":smile_score_l,"top_l":top_l,"left_l":left_l,"size_l":size_l}
    return info 
def analysis_class(url,fe1,role="teacher"):
    #    {1:{"video":{"student_face_url":null,"teacher_face_url":null,"student_is_happy":null,"teacher_is_happy":null,"teacher_hand_gesture":null,"student_is_half_face":false,"teacher_is_half_face":false,"teacher_face_special":0.500000,"student_is_eye_closed":null,"teacher_is_eye_closed":null,"teacher_face_landmark":null,"student_face_landmark":null}}}
    info={}
    info[role]={} 
    try:
        if role=="teacher":
            info[role]=analysis_teacher(url,fe1)
        if role=="student":
            info[role]=analysis_student(url,fe1)
    except Exception as e:
        print("errro:%s"%e)
        info[role]['smile_image']=""

    info[role]['smile_image']=""
    zprint("%s"%info)
    
    return info
if __name__=="__main__":
    teacher_url="http://192.168.48.55/mp4/vipkid_jz30bdd2f5cbf849a39d2e07a4ebd95393_f_1530358219388_t_1530359737548.mp4"
    student_url="http://192.168.48.55/mp4/vipkid_jzbe5c90fd4a184fceab484531c77e9342_f_1530358219388_t_1530359737548.mp4"
    #analysis_class(teacher_url,student_url)
    analysis_class(teacher_url,fe0,"teacher")
    analysis_class(student_url,fe0,"student")
