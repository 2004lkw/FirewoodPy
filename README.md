# FirewoodPy
Logging module I wrote for custom logging.  Buffers and stacks as needed.

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
