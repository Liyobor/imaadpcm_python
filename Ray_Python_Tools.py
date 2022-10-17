from genericpath import isdir
from gettext import find
from operator import contains
import os
from pydub import AudioSegment

class WavSlicer:

    def __init__(self) -> None:
        self.__sound = None
        self.__outPath = ''
        self.max_dBFS = None
        self.wav_duration = None
        self.soundAfterSlice = None
    
    def loadWavFile(self,file:str,outPutSampleRate:int,sampler_bit:int = 16,channels:int = 1):
        self.__sound = None
        self.__sound = AudioSegment.from_wav(file)
        self.__sound = self.__sound.set_frame_rate(outPutSampleRate)
        self.__sound = self.__sound.set_sample_width(int(sampler_bit/8))
        self.__sound = self.__sound.set_channels(channels)
        self.sound = self.__sound
        self.wav_duration = len(self.__sound)
    


    def cut(self,startMilliSecond:int,endMilliSecond:int):
        self.soundAfterSlice = self.__sound[startMilliSecond:endMilliSecond]
    
    def exportCuttedWav(self,newFileName:str,outputPath:str=None):
        tempPath = outputPath
        if outputPath != None:
            subPathParts = []
            while(not os.path.exists(tempPath)):
                subPathParts.append(tempPath[tempPath.rindex('\\'):])
                tempPath = tempPath[0:tempPath.rindex('\\')]
            subPathParts.reverse()
            for subPath in subPathParts:
                tempPath+=subPath
                os.makedirs(tempPath)
            self.__outPath = outputPath+'\\'+newFileName
        else:
            self.__outPath = newFileName
        self.soundAfterSlice.export(self.__outPath,format = "wav")
                



class SimpleFileExplorer:

    def __init__(self,path=os.getcwd()) -> None:
        self.__path = path
        self.files = []
        '''
        This contains files list
        '''
        self.__getFiles()

        self.dirs = []
        '''
        This contains directory list
        '''
        self.__getDirs()


        

    def __getDirs(self):
        dirs = []
        for item in os.scandir(self.__path):
            if item.is_dir():
                dirs.append(item.path)

        self.dirs = dirs
        

    def __getFiles(self):
        files = []
        for item in os.scandir(self.__path):
            if item.is_file():
                files.append(self.__path+'\\'+item.name)
        self.files = files
    
    def getCurrentPath(self)->str:
        print(self.__path)
        return self.__path
    

    def walk(self,path:str):
        '''
        input '..' to the previous directory
        '''
        if(path == ".."):
            lastIndex = self.__path.rindex("\\")
            newPath = self.__path[0:lastIndex]
        elif path.count('\\')>=1 and path.find('\\')==2:
            newPath = path
        else:
            if(self.__path[-1]=='\\'):
                newPath = self.__path +path
            else:
                newPath = self.__path+'\\'+path
            
        if(os.path.isdir(newPath)):
            self.__path = newPath
        else:
            raise Exception("Path doesn't exist!")

        self.__getDirs()
        self.__getFiles()

