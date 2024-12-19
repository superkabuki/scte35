# <s>threefive</s>
![image](https://github.com/user-attachments/assets/b03595f6-04b0-4fc1-a5b7-ccc6ec3394d7)


threefive continued.  SCTE-35 for the People.
# Now with Super Advanced Error Detection and Stuff. 
* Does not generate Fatal errors, it won't break your process.
* Displays what is in error and how to correct it.
* Works in the cli
* Works in code.
![image](https://github.com/user-attachments/assets/581e0081-0c9d-4f9c-87a2-dd7f4cf3ce8c)

![image](https://github.com/user-attachments/assets/6a430e12-19b8-422e-9545-b14ecdd7ce60)


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
* [__Parse __MPEGTS__ streams for __SCTE-35__](#streams)
* [Parse __SCTE-35__ in __hls__](#hls)
* [Display __MPEGTS__ __iframes__](#iframes)
* [Display raw __SCTE-35 packets__ from __video streams__](#packets)
* [__Repair SCTE-35 streams__ changed to __bin data__ by __ffmpeg__](#sixfix)


### `Inputs` 
* the cli can __decode SCTE-35__ from
 * [__Base64__](#base64)
 * [__Hex,__](#hex)
 * [__HLS,__](#hls)
 * [__JSON,__](#json)
 * [__Xml,__](#xml)
 * [__Xml+Bin__](#xmlbin)
 * [__MPEGTS Streams__](#streams)

* Most __inputs__ are __auto-detected.__ 
* __stdin__ is __auto selected__ and __auto detected.__
* __SCTE-35 data is printed to stderr__
* __stdout is used when piping video__
#### `Base64` 
* parse SCTE-35 encoded in Base64
```rebol
threefive3 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU='
```

#### `Hex`
* parse SCTE-35 encoded in Hex
```rebol
threefive3 0xfc302c00000003289800fff00a05000000017f5f999901010011020f43554549000000007f8001003500002d974195
```

#### `HLS`

* parse SCTE-35 from HLS manifests and segments
```rebol
threefive3 hls https://example.com/master.m3u8
```

#### `Json`

```rebol
cat json.json | threefive3
```
#### `Xml`
* you can make a xml.xml file like this:
  * redirect 2 (stderr) to the file 
```awk
./threefive3  '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' xml 2> xml.xml
```
* pass in
```rebol
threefive3  < xml.xml
```
#### `Xmlbin`

```rebol
threefive3 < xmlbin.xml
```
___
### `Outputs`

 * the cli can __encode SCTE-35__ to
 * [__Base64__](#base64-1)
 * [__Bytes__](#bytes)
 * [__Hex,__](#hex-1)
 * [__HLS,__](#hls-1)
 * [__JSON,__](#json-1)
 * [__Xml,__](#xml-1)
 * [__Xml+Bin__](#xmlbin-1)

* default output is `json`

#### json
```rebol
threefive3 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU='
```

#### `base64`
```rebol
threefive3 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' base64
```
#### `bytes`
```rebol
threefive3 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' bytes
```
#### `hex`
```rebol
threefive3 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' hex
```
#### `int`
```rebol
threefive3 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' int
```
#### `xml`
```rebol
threefive3 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' xml
```
#### `xml+bin`
```rebol
threefive3 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' xmlbin
```
___
## Streams
### `File and Network Protocols`

#### `File` 
```rebol
threefive3 video.ts
```
#### `Http(s)` 
```rebol
threefive3 https://example.com/master.m3u8
```
#### `Multicast`
```rebol
threefive3 udp://@235.35.3.5:9999
```
#### `stdin`
```rebol
cat video.ts | threefive3
```
#### `Udp Unicast`
```rebol
threefive3 udp://10.0.0.7:5555
```
___

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

