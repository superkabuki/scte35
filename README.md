# `scte35`
threefive continued.  SCTE-35 for the People.

# `Install`
* python3 via pip
```py3
python3 -mpip install scte35
```
* pypy3 
```py3
pypy3 -mpip install scte35
```
* from the git repo
```js
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
```asm
scte35 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU='
```

#### `Hex`
* parse SCTE-35 encoded in Hex
```smalltalk
scte35 '0xfc302c00000003289800fff00a05000000017f5f999901010011020f43554549000000007f8001003500002d974195'
```

#### `HLS`

* parse SCTE-35 from HLS manifests and segments
```lua
scte35 hls https://example.com/master.m3u8
```

#### `Json`

```lua
cat json.json | scte35
```
#### `Xml`

```lua
scte35  < xml.xml
```
#### `Xml+bin`

```lua
scte35 < xmlbin.xml
```
___
### `Output`

* Base64, Bytes, Hex, Json, Int, Xml, or Xml+bin can be specified as output.
* default output is `json`
```json
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x03",
        "sap_details": "No Sap Type",
        "section_length": 44,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 2.3,
        "cw_index": "0x00",
        "tier": "0x0fff",
        "splice_command_length": 10,
        "splice_command_type": 5,
        "descriptor_loop_length": 17,
        "crc": "0x2d974195"
  ...

```

#### `base64`
```lua
scte35 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' base64
```
#### `bytes`
```lua
scte35 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' bytes
```
#### `hex`
```lua
scte35 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' hex
```
#### `int`
```lua
scte35 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' int
```
#### `xml`
```lua
scte35 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' xml
```
#### `xml+bin`
```xml
scte35 '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' xmlbin
```
___

### `File and Network Protocols`

#### `File` 
```lua
scte35 video.ts
```
#### `Http(s)` 
```lua
scte35 https://example.com/master.m3u8
```
#### `Multicast`
```lua
scte35 udp://@235.35.3.5:9999
```
#### `stdin`
```lua
cat video.ts | scte35
```
#### `Udp Unicast`
```lua
scte35 udp://10.0.0.7:5555
```
___

### `hls`
* parse hls manifests and segments for SCTE-35
```lua
scte35 hls https://example.com/master.m3u8
```
___
### `Iframes`
* Show iframes PTS in an MPEGTS video
```lua
scte35 iframes https://example.com/video.ts
```
___
### `packets`   
* Print raw SCTE-35 packets from multicast mpegts video
```lua
scte35 packets udp://@235.35.3.5:3535
```
___
### `proxy`   
* Parse a https stream and write raw video to stdout
```lua
scte35 proxy video.ts
```
___
### `pts`    
* Print PTS from mpegts video
```lua
 scte35 pts video.ts
```
___
### `sidecar`  
* Parse a stream, write pts,write SCTE-35 Cues to sidecar.txt
```lua
  scte35 sidecar video.ts
```
___
### `sixfix`  
* Fix SCTE-35 data mangled by ffmpeg
```lua
 scte35 sixfix video.ts
```
___
### `show`  

* Probe mpegts video _( kind of like ffprobe )_
```lua
 scte35 show video.ts
```
___
### `version`     
* Show version
```lua
 scte35 version
```
___
### `help`        
* Help
```lua
 scte35 help
```
___
