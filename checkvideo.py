import os
import subprocess
import sys
import glob
import logging

logging.basicConfig(filename='check.log', level=logging.DEBUG,format='%(asctime)s:%(message)s')
ffmpegpath='ffmpeg'

def checkOneFile(path0):
    #check video file using FFmpeg  video conversion if no error message was outputed to STDOUT
    cmd=[ffmpegpath,'-v','error','-i',path0,'-vf','scale=160:-1','-vcodec','h264_qsv','-f','null','-']
    result=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    if len(result.stdout) > 0:
        return False
    else:
        return True
    #

if __name__=='__main__':
    if len(sys.argv) < 2:
        sys.exit(-1)
    # find target file in each Arg(path)
    filelist=[]
    for i in range(1,len(sys.argv)):
        rootpath=sys.argv[i]
        if not os.path.exists(rootpath): #check if path exists 
            continue
        #if args is video file,add them to file list.
        if os.path.isfile(rootpath):
            if (os.path.basename(rootpath)[-4:]=='.mp4')or\
               (os.path.basename(rootpath)[-4:]=='.wmv'):
                filelist.append(rootpath)
                continue
        #if args is dir,find video files in it.
        tmplist=glob.glob(os.path.join(rootpath,'**/*.mp4'),recursive=True)
        if len(tmplist)>0:
            filelist.extend(tmplist)
        tmplist=glob.glob(os.path.join(rootpath,'**/*.wmv'),recursive=True)
        if len(tmplist)>0:
            filelist.extend(tmplist)
    #main routine
    logging.info('%s','Check start.')
    for filename in filelist:
        if checkOneFile(filename):
            logging.info('%s',filename+":OK.")
        else:
            print('there are errors in '+filename)
            logging.warning('%s',filename+':NG.')
    logging.info('%s','Check end.')
