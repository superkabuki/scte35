# `scte35`
threefive continued.  SCTE-35 for the People.

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

### `Decoding SCTE-35` 
* the cli can __decode SCTE-35__ from MPEGTS Streams, Base64, Hex, HLS, JSON, Xml, and Xml+Bin formats.
* Most __inputs__ are __auto-detected__ 

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

```rebol
scte35  < xml.xml
```
#### `Xml+bin`

```rebol
scte35 < xmlbin.xml
```
___
### `Output`

* Base64, Bytes, Hex, Json, Int, Xml, or Xml+bin can be specified as output.
* default output is `json`
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
