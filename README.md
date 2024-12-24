![image](https://github.com/user-attachments/assets/adae03a1-9f85-403e-9dce-d134e0996903)



> I wrote threefive because I couldn't find any SCTE-35 tools. There were a few libraries, but SCTE-35 wasn't their focus,
> and they required writing several hundred lines of code to do anything. I think a library should save you time.
# Why threefive3, why not just threefive?
* __Answer #1__ Github F2A'ed out of my account, and I have no idea where I put the recovery codes. I have more than one Internet account, where I am supposed to keep all this data? Should I store in some company's cloud so they can read it or give it away to Eastern European script kiddies? F2A is complete nonsense. It doesn't matter how secure it is, if a security measure prevents me from accessing my account, that's not secure, that's locked out.
* __Answer #2__     Two repos with the same name, would be confusing.
* __Answer #3__ I wanted to rethink everything. After going through the code, I kept about 75% of it. I completely rewrote the Xml parser,I did a lot of work with the Cue class, HLS, and really tuned up the cli. The cli is amazing and super easy to use.
*  __Answer #4__  I came up with a really cool name, but it wasn't available on pypi.org for a package name.
*  __Answer #5__  Really, I was just getting a little bored with the whole thing, I just wanted to shake things up a little, keep it fun.
*  __Answer #6__ Have you seen chewy Tic Tacs? They're just mini jelly beans.
*  __Answer #7__ I'll tell you the truth, everything is a lie.
  
# How do I upgrade my code to threefive3?
> Despite making a lot of changes, the api remains. threefive3 is pretty much a drop in replacement for threefive. I used sed to upgrade my code.
```js
sed -e 's/threefive/threefive3/g'
```
> One thing to note, calling load or decode is no longer necessary for the Cue class, however, the methods are there in case you do call them.
>
> 
# Is threefive3 faster than threefive?
* __threefive__ vs. __threefive3__ vs. __threefive3 next release__
![image](https://github.com/user-attachments/assets/7624c482-2a52-4d2b-83ff-25bac4720a34)


* The next release of __threefive3 parses 3.7GB of MPEGTS video in just 3.422 seconds. Over 1GB a second.__
* _testing was done on a beatup chrome book reporting 5GB of RAM running Debian Sid_
  
---

# Now with Super Advanced Error Detection and Stuff. 
* This is super cool. 
* Does not generate Fatal errors, it won't break your process.
* Displays what is in error and how to correct it.
* Works in the cli
* Works in code.
  ![image](https://github.com/user-attachments/assets/50331e73-cd0a-46d6-b265-1b212d625737)


# Issues and Bugs.
* If you think you have a bug, I'll quickly fix it, but first I need you to prove it to me. Show me the entire error message, the code you're running, and the SCTE-35.
---
# Special Requests 
* If need some work done, this is what I do for a living, you can hire me.
* If you want to discuss your project open an issue and I'll send you my contact info.
---

# `Install`
* python3 via pip
```rebol
python3 -mpip install threefive3
```
* pypy3 
```rebol
pypy3 -mpip install threefive3
```
* from the git repo
```rebol
git clone https://github.com/superkabuki/scte35.git
cd scte35
make install
```
___

# `The Cli tool`
> The cli audetects data being available on stdin and that allows it to autodetect the SCTE-35 format as well as MPEGTS steams. Now every SCTE-35 data format, except hls, is autodetected on the commandline, as well as stdin.HLS requires the `hls` ketyword.

### The cli tool installs automatically with pip or the Makefile.


* [__SCTE-35 Inputs__](#inputs)
* [__SCTE-35 Outputs__](#outputs)
* [Parse __MPEGTS__ streams for __SCTE-35__](#streams)
* [Parse __SCTE-35__ in __hls__](#hls)
* [Display __MPEGTS__ __iframes__](#iframes)
* [Display raw __SCTE-35 packets__ from __video streams__](#packets)
* [__Repair SCTE-35 streams__ changed to __bin data__ by __ffmpeg__](#sixfix)


# `Inputs`

* Most __inputs__ are __auto-detected.__ 
* __stdin__ is __auto selected__ and __auto detected.__
* __SCTE-35 data is printed to stderr__
* __stdout is used when piping video__

| Input Type |     Cli Example                                                                                             |
|------------|-------------------------------------------------------------------------------------------------------------|
| __Base64__     |  `threefive3 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU='`
| __Hex__        |`threefive3 0xfc301600000000000000fff00506fed605225b0000b0b65f3b`|
| __HLS__         |`threefive3 hls https://example.com/master.m3u8`                                                             |
| __JSON__        |`threefive3 < json.json`  |
| __Xml__         | `threefive3  < xml.xml`                                                                                     |
| __Xmlbin__      | `threefive3 < xmlbin.xml`                                                                                   |

# Streams

|Protocol       |  Cli Example                                                                                                                                       |
|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
|  File         |   `threefive3 video.ts`                                                                                                                            |
|  Http(s)      |   `threefive3 https://example.com/video.ts`                                                                                                        |
|  Stdin        |  `threefive3 < video.ts`            |
|  UDP Multicast|  `threefive3 udp://@235.35.3.5:9999`                                                                          |
|  UDP Unicast  |                                                                      `threefive3 udp://10.0.0.7:5555`                                              |
|  HLS          |                                                                                                    `threefive3 hls https://example.com/master.m3u8`|
|               |                                                                                                                                                    |


### Outputs
* output type is determined by the key words __base64, bytes, hex, int, json, xml, and xmlbin__.
* __json is the default__.
* __Any input (except HLS,) can be returned as any output__
  * examples __Base64 to Hex__, or  __Mpegts to Xml__, etc...) 


| Output Type | Cli Example         |
|-------------|----------------------------------------------------------|
|__Base 64__     |                                                                                                                                                                    `threefive3 0xfc301600000000000000fff00506fed605225b0000b0b65f3b  base64  `                                                                                                                                                                                                                                                                                                                                         |
| __Bytes__       |                                                                                 `threefive3 0xfc301600000000000000fff00506fed605225b0000b0b65f3b  bytes`                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Hex         | `threefive3 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU='  hex`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Integer     |                                                                                                                                                                                                                                                       `threefive3 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU='  int`   |
| JSON        |                                                                                                                                                                                                                                                                                                              `threefive3 0xfc301600000000000000fff00506fed605225b0000b0b65f3b json ` |
| Xml         |                                                                                                                                                                                                                                                                                                                                                                                                                        `threefive3 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' xml `                                                                                 `         |
| Xml+bin     |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `threefive3 0xfc301600000000000000fff00506fed605225b0000b0b65f3b xmlbin   `      |`

### `hls`
* parse hls manifests and segments for SCTE-35
```rebol
threefive3 hls https://example.com/master.m3u8
```
___
### `Iframes`
* Show iframes PTS in an MPEGTS video
```rebol
threefive3 iframes https://example.com/video.ts
```
___
### `packets`   
* Print raw SCTE-35 packets from multicast mpegts video
```rebol
threefive3 packets udp://@235.35.3.5:3535
```
___
### `proxy`   
* Parse a https stream and write raw video to stdout
```rebol
threefive3 proxy video.ts
```
___
### `pts`    
* Print PTS from mpegts video
```rebol
 threefive3 pts video.ts
```
___
### `sidecar`  
* Parse a stream, write pts,write SCTE-35 Cues to sidecar.txt
```rebol
  threefive3 sidecar video.ts
```
___
### `sixfix`  
* Fix SCTE-35 data mangled by ffmpeg
```rebol
 threefive3 sixfix video.ts
```
___
### `show`  

* Probe mpegts video _( kind of like ffprobe )_
```rebol
 threefive3 show video.ts
```
___
### `version`     
* Show version
```rebol
 threefive3 version
```
___
### `help`        
* Help
```rebol
 threefive3 help
```
## [iodisco.com/scte35](https://iodisco.com/scte35)
[![image](https://github.com/user-attachments/assets/28d228c5-56e2-41d3-a053-eebd3af958f1)
![image](https://github.com/user-attachments/assets/07c52c21-e83e-438d-91b0-6f502f0d1d43)](https://iodisco.com/scte35)
___

