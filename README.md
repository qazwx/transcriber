### Local speech-to-text script

It is not accurate. Is not fast (although I tried parallelizing loading audio). 
It works, mostly...


#### Install

> pip install SpeechRecognition      
> git clone https://www.github.com/qazwx/transcriber.git       
> cd transcriber        
> chmod u+x transcriber.py      

#### Use

> ./transcriber/transcriber.py /path/to/audio/file.mp3


#### Performance

All tests rely on ``http://www.obamadownloads.com/mp3s/dnc-2004-speech.mp3`` (about 13 minutes) as audio-test.

| Standard 	|  Parallel (8-cores) + Chunking* 	| Chunking* 	| Chunking✝  | 
|---	    |---	                            |---	        | ---         |
|  >600s    |  	~224s                           | ~428s         | ~461s       |
|  >600s    |   ~226s                           | ~432s         | ~463s       |



*: Chunks were 60-seconds long.      
✝: Chunks were 10-seconds long.
