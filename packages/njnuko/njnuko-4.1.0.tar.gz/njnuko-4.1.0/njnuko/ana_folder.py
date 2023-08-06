import os
import os.path
import shutil
import time
import datetime
import stat
from PIL import Image,ImageFile
from PIL import ImageChops
from PIL.ExifTags import TAGS
import locale
import filetype
import hashlib
import pymysql
import time
import psycopg2
import csv
import sqlite3
locale.getdefaultlocale()
import csv

def getDB(a):
    if a == 1:
        conn = pymysql.connect(host='home.njnuko.top', port=33066, user='root', passwd='admin',db='nas_files')
    elif a == 0:
        conn =  conn = sqlite3.connect('nas_files.db')
    elif a == 2:
        conn = psycopg2.connect(host='home.njnuko.top', port=25432, user='ko', password='231231',database='nas_files')
    return conn


def ana(folder):
    seq = 1
    dict = {}
    log = os.path.join(folder,'anf_list.log')
    out = open(log,'a')
    wt = csv.writer(out)    
    for i in os.listdir(folder):
            dict[seq] = i
            wt.writerow([seq,dict[seq]])
            seq = seq + 1
    out.close()
    return dict

    

def file_move(frfolder,file1,dest,log):

    if os.path.exists(os.path.join(dest,file1)):
        the_md5=hashlib.md5()
        f1 = open(os.path.join(frfolder,file1), 'rb')
        the_md5.update(f1.read())
        hash1 = the_md5.hexdigest()
        f2 = open(os.path.join(dest,file1), 'rb')
        the_md5.update(f2.read())
        hash2 = the_md5.hexdigest()
        f1.close()
        f2.close()

        if hash1 == hash2:
            with open(log,'a') as f:
                writer = csv.writer(f)
                writer.writerow('delete',os.path.join(frfolder,file1),os.path.join(dest,file1),hash1)
                f.close()
            os.remove(os.path.join(frfolder,file1))


    else:
        the_md5=hashlib.md5()
        f1 = open(os.path.join(frfolder,file1), 'rb')
        the_md5.update(f1.read())
        hash1 = the_md5.hexdigest()
        f1.close()
        
        with open(log,'a') as f:
            writer = csv.writer(f)
            writer.writerow('delete',os.path.join(frfolder,file1),os.path.join(dest,file1),hash1)
            f.close()
        shutil.move(os.path.join(frfolder,file1),dest)



            
def class_bytype(folder,dstfold):
    log = os.path.join(dstfold,'class_bytype.log')
    if os.path.exists(log):
        os.remove(log)
    for i in os.listdir(folder):
        if os.path.isdir(os.path.join(folder,i)):
            class_bytype(os.path.join(folder,i),dstfold)
        else:
            if filetype.guess(i) is not None:
                type = filetype.guess(i)
                if not (os.path.exists(os.path.join(dstfold,type))):
                    os.makedirs(os.path.join(dstfold,type))
                file_move(folder,i,os.path.join(dstfold,type),log)

            else:
                type = 'None'
                if not (os.path.exists(os.path.join(dstfold,type))):
                    os.makedirs(os.path.join(dstfold,type))
                file_move(folder,i,os.path.join(dstfold,type),log)




def gettime(file):
    """Get embedded EXIF data from image file."""
    ret = {}
    print(file)
    print('--------------------------------------------')
    try:
        if filetype.guess(file).extension in ('jpg','jpeg','gif','png','bmp'):    
                try:
                    img = Image.open(file)
                    if hasattr( img, '_getexif' ):
                        try:
                            exifinfo = img._getexif()
                        except:
                            exifinfo = None
                        if exifinfo != None:
                            for tag, value in exifinfo.items():
                                decoded = TAGS.get(tag, tag)
                                ret[decoded] = value
                        else:
                            timeArray = time.localtime(os.path.getctime(file))
                            otherStyleTime = time.strftime("%Y-%m-%d-%H%M%S", timeArray)
                            return str(otherStyleTime).replace(':','-').replace(' ','_')
                except IOError:
                    print('IOERROR/ValueError ' + file)
    except ValueError:
        print('ValueError ' + file)

            
    if ret.get('DateTimeOriginal') != None:
        cd = ret.get('DateTimeOriginal')[0:7].replace(':','-').replace(' ','')
        return cd
    else:
        timeArray = time.localtime(os.path.getctime(file))
        otherStyleTime = time.strftime("%Y-%m-%d-%H%M%S", timeArray)
        return str(otherStyleTime).replace(':','-').replace(' ','_')
#        print('creation date: '+os.path.getctime(fname).replace(':','-').replace(' ','_') ) 
#        return os.path.getctime(fname).replace(':','-').replace(' ','_')   


def class_bytime(folder,desfold):
    log = os.path.join(desfold,'class_bytime.log')
    if os.path.exists(log):
        os.remove(log)
    for i in os.listdir(folder):
        if os.path.isdir(os.path.join(folder,i)):
            class_bytime(os.path.join(folder,i),desfold)
        else:            
            a = gettime(os.path.join(folder,i))
            if not os.path.exists(os.path.join(desfold,a)):
                os.makedirs(os.path.join(desfold,a))
            file_move(folder,i,os.path.join(desfold,a),log)

def main():
    pass
if __name__ == '__main__':
    main()
