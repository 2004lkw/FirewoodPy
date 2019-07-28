import random
from datetime import datetime

'''
    Logging class built by Larry Williams.
    This class is meant to serve as a logging module which you can import into your projects.  It supports
    error level logging and buffered logging which is a direct result of giving log information multiple times
    and "compressing" it into +##'s.  
    Time stamps are automatic and places at the beginning of the event.  an example: 
        13:32:04.515958 : 2 : (logged with errors?)
    Buffered "compressed" option example:
        13:32:04.520947 : 1 : Log event. +7 [Event End Time: 13:32:04.521978]
    
    
    The main functions the dev will use are:
        the constructor -- call with (STRING: filename(and path if needed), BOOLEAN: optional for buffer use)
                                                                                    ^ defaults to FALSE.
        .writeLog(STRING: Information to write.)
        .writeLogE(INT: Error level to write, STRING: Information to write.)
        .flush() -- Only needed if you are using the buffer option.  Call before termination of the program.  
'''


class Firewood:
    # -----------------------------------------------------------------------------------------------------------------
    #   Member variables for this class.
    fileName = ""  # Filename we are writing to.
    bufferStr = ""  # Buffer string last used
    currentStr = ""  # Current String being eval/written
    usingBuffer = False  # Using the buffer feature?
    myCount = 0  # Count for how many +1's
    NO_LOG_LEVEL = -1  # CONST for NOT logging error level.
    bufferTimeStart = ""  # string that contains the start of the buffer time.

    def __init__(self, filename, useBuffer=False):
        # Class constructor.  buffer use defaults to false if omitted from the call to this.
        self.fileName = filename
        if useBuffer:
            self.usingBuffer = True

    def writeLog(self, strToWrite1):
        # this is an overload for NOT having a error level below.
        #   This passes NO_LOG_LEVEL so that the writeLogE func ignores the error level.
        """
        #   Uncomment this if you wish to enforce buffered option strictly.
        if self.usingBuffer:
            # if using buffer is turned on and you call this, this will kick it back because there is no err lvl.
            return False
        """
        return self.writeLogE(self.NO_LOG_LEVEL, strToWrite1)

    def writeLogE(self, errorLvl, strToWrite):
        # ---- Writes to the log with an error level.
        # errorLvl is meant as a user-defined error level event of logging.
        # strToWrite is the string to write to the log.

        # first, test for a blank write string.
        if not strToWrite:
            return False

        errorLvlText = ""

        try:  # to open the file....
            fileNow = open(self.fileName, "a")
        except:  # intentionally set as a blank except!!
            # Since open file failed....
            # without disrupting program flow, return an error code of FALSE
            return False

        if not errorLvl == self.NO_LOG_LEVEL:
            # if using error level, include that in the log.
            errorLvlText = str(errorLvl) + " : "

        if self.usingBuffer:
            # using the buffer.
            # since the error level is part of log, we should attach it here.
            strToWrite = errorLvlText + strToWrite

            if not self.bufferStr:
                # using bufferStr but there's nothing in it yet.   This check keeps us from erroneous
                # lines from snowing up.
                self.bufferStr = strToWrite
                return True
            # test if this has been passed before.
            if self.bufferStr == strToWrite:
                # the bufferStr matches, don't write yet.
                self.bufferTimeStart = self.timeMe()  # get the START time of the event.
                if self.myCount == 0:
                    self.myCount = 2
                else:
                    self.myCount = self.myCount + 1
                return True  # exit because we know that it is +1'd
            else:
                # bufferStr doesn't match the new text so lets write what we have.
                if self.myCount > 0:
                    # there is more than one statement so we write the + version.
                    builtString = self.bufferTimeStart + " : " + self.bufferStr + " +" + str(
                        self.myCount) + " [Event End Time: " + self.timeMe() + "]\n"
                    fileNow.write(builtString)
                    self.myCount = 0  # restart the my count since we have new logging info.
                    self.bufferStr = strToWrite  # move current string to buffer string.
                    # Note!  It is important to call .flush() before you exit your program or the
                    # buffer never gets written.
                else:
                    # this statement was unique from the last.  Write normally.
                    builtString = self.timeMe() + " : " + self.bufferStr + "\n"
                    fileNow.write(builtString)
                    self.bufferStr = strToWrite  # move current string to buffer string.
        else:
            # not using buffer.
            fileNow.write(self.timeMe() + " : " + errorLvlText + strToWrite + "\n")
        fileNow.close()
        return True

    def flush(self):
        # call this if we need to flush bufferStr
        if self.usingBuffer:
            self.writeLogE(-99, "[SYSTEM BUFFER FLUSH]")
        return True

    def timeMe(self):
        # function to return the time.
        # timeReturn = datetime.now().strftime('%H:%M:%S')
        timeReturn = str(datetime.now().time())
        return timeReturn
