import os
import subprocess
import sys
import glob
import logging

logging.basicConfig(filename='check.log', level=logging.DEBUG,format='%(asctime)s:%(message)s')
ffmpegpath='ffmpeg'

def changeOneFile(path0,path1):
    #check video file using FFmpeg  video conversion if no error message was outputed to STDOUT
    #cmd=[ffmpegpath,'-v','error','-i',path0,'-vf','scale=-1:720','-vcodec','h264_qsv','-qmax','30','-f','mp4',path1]
    #cmd=[ffmpegpath,'-v','error','-i',path0,'-vf','scale=-1:720','-vcodec','h264_qsv','-f','mp4',path1]
    #cmd=[ffmpegpath,'-v','error','-i',path0,'-vf','scale=-1:720','-vcodec','h264_qsv','-qmax','30',
    #    '-f','mp4','-an','-pass','1',path1]
    #result=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    #if len(result.stdout) > 0:
    #    return False
    cmd=[ffmpegpath,'-v','error','-i',path0,'-f','mp3',path1]
        #'-f','mp4','-pass','2','-ab','1792k','-y',path1]
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
    logging.info('%s','Convert audio start.')
    #outputRoot=r'G:\Converted'
    outputRoot=r'../../data/audio/'
    for filename in filelist:
        basename1=os.path.basename(filename)
        rootname1=os.path.dirname(filename)
        #tgtDir=rootname1.replace("Download","Converted")
        #if not os.path.exists(tgtDir):
        #    os.makedirs(tgtDir)
        basename2=os.path.basename(rootname1)
        outputDir=os.path.join(outputRoot,basename2)
        if os.path.basename(filename).split('.')[1]=='wmv':
            if not os.path.exists(outputDir):
                os.makedirs(outputDir)
            tgtFileName=os.path.join(outputDir,basename2+'_'+basename1[:-4]+'.mp3')
        if os.path.basename(filename).split('.')[1]=='mp4':
            tgtFileName=os.path.join(outputRoot,basename1[:-4]+'.mp3')
        if os.path.exists(tgtFileName):
            continue

        if changeOneFile(filename,tgtFileName):
            logging.info('%s',filename+":OK.")
        else:
            print('there are errors in '+filename)
            logging.warning('%s',filename+':NG.')
    logging.info('%s','Convert 2 audio mp3 end.')
