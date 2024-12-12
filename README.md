# `scte35`
threefive continued.  SCTE-35 for the People.
# Now with Super debug, everywhere!
![image](https://github.com/user-attachments/assets/581e0081-0c9d-4f9c-87a2-dd7f4cf3ce8c)



 

# `Install`
* python3 via pip
```rebol
python3 -mpip install scte35
```
* pypy3 
```rebol
pypy3 -mpip install scte35
```
* from the git repo
```rebol
git clone https://github.com/superkabuki/scte35.git
cd scte35
make install
```
___


# `The Cli tool`
> The cli was good, but it has improved dramatically, it has really come together.Now, the cli audetects data being available on stdin and that allows it to autodetect the SCTE-35 format as well as MPEGTS steams. Now every SCTE-35 data format, except hls, is autodetected on the commandline, as well as stdin.HLS requires the `hls` ketyword.

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
scte35 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU='
```

#### `Hex`
* parse SCTE-35 encoded in Hex
```rebol
scte35 0xfc302c00000003289800fff00a05000000017f5f999901010011020f43554549000000007f8001003500002d974195
```

#### `HLS`

* parse SCTE-35 from HLS manifests and segments
```rebol
scte35 hls https://example.com/master.m3u8
```

#### `Json`

```rebol
cat json.json | scte35
```
#### `Xml`
* you can make a xml.xml file like this:
  * redirect 2 (stderr) to the file 
```awk
./scte352  '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' xml 2> xml.xml
```
* pass in
```rebol
scte35  < xml.xml
```
#### `Xmlbin`

```rebol
scte35 < xmlbin.xml
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
scte35 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU='
```

#### `base64`
```rebol
scte35 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' base64
```
#### `bytes`
```rebol
scte35 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' bytes
```
#### `hex`
```rebol
scte35 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' hex
```
#### `int`
```rebol
scte35 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' int
```
#### `xml`
```rebol
scte35 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' xml
```
#### `xml+bin`
```rebol
scte35 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' xmlbin
```
___
## Streams
### `File and Network Protocols`

#### `File` 
```rebol
scte35 video.ts
```
#### `Http(s)` 
```rebol
scte35 https://example.com/master.m3u8
```
#### `Multicast`
```rebol
scte35 udp://@235.35.3.5:9999
```
#### `stdin`
```rebol
cat video.ts | scte35
```
#### `Udp Unicast`
```rebol
scte35 udp://10.0.0.7:5555
```
___

### `hls`
* parse hls manifests and segments for SCTE-35
```rebol
scte35 hls https://example.com/master.m3u8
```
___
### `Iframes`
* Show iframes PTS in an MPEGTS video
```rebol
scte35 iframes https://example.com/video.ts
```
___
### `packets`   
* Print raw SCTE-35 packets from multicast mpegts video
```rebol
scte35 packets udp://@235.35.3.5:3535
```
___
### `proxy`   
* Parse a https stream and write raw video to stdout
```rebol
scte35 proxy video.ts
```
___
### `pts`    
* Print PTS from mpegts video
```rebol
 scte35 pts video.ts
```
___
### `sidecar`  
* Parse a stream, write pts,write SCTE-35 Cues to sidecar.txt
```rebol
  scte35 sidecar video.ts
```
___
### `sixfix`  
* Fix SCTE-35 data mangled by ffmpeg
```rebol
 scte35 sixfix video.ts
```
___
### `show`  

* Probe mpegts video _( kind of like ffprobe )_
```rebol
 scte35 show video.ts
```
___
### `version`     
* Show version
```rebol
 scte35 version
```
___
### `help`        
* Help
```rebol
 scte35 help
```
___
