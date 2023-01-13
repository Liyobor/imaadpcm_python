from adpcm import Adpcm


class Adpcm3(Adpcm):
    

    def encode(self,inData):
        valpred = self.encodeState.valprev
        index = self.encodeState.index
        step = self._ss_table[index]
        diff = inData - valpred
        if(diff<0):
            delta = 8
            diff = (-diff)
        else:
            delta = 0
        vpdiff = (step >> 3)
        if(diff>=step):
            delta |= 4
            diff -= step
            vpdiff += step
        step >>= 1
        if(diff>=step):
            delta |=2
            diff -=step
            vpdiff+=step
        step >>=1
        if(diff>=step):
            delta |= 1
            vpdiff += step
        if ((delta &8)>0):
            valpred -= vpdiff
            if (valpred<-32768):
                valpred = -32768
        else:
            valpred+=vpdiff
            if(valpred>32767):
                valpred = 32767
        index += self._i_table[delta]
        if(index<0):
            index = 0
        elif(index>88):
            index = 88
        step = self._ss_table[index]
        self.encodeState.valprev = valpred
        self.encodeState.index = index
        return delta

    def decode(self,delta):
        valpred = self.decodeState.valprev
        index = self.decodeState.index
        step = self._ss_table[index]
        
        index += self._i_table[delta]
        if(index<0):
            index = 0
        elif(index>88):
            index = 88

        vpdiff = step >> 3
        if((delta&4)>0):
            vpdiff += step
        if((delta&2)>0):
            vpdiff += step >> 1
        if((delta&1)>0):
            vpdiff += step >> 2

        if((delta&8)>0):
            valpred-=vpdiff
            if(valpred<-32768):
                valpred = -32768
        else:
            valpred+=vpdiff
            if(valpred>32767):
                valpred = 32767

        step = self._ss_table[index]
        self.decodeState.valprev = valpred
        self.decodeState.index = index
        

        # return valpred
        if(valpred<0):
            return valpred/32768
        elif(valpred>0):
            return valpred/32767
        else:
            return valpred
