# `fu`
threefive continued.  SCTE-35 for the People.


# `The Cli tool`
> One thing I hate about video is all the complexity. I tried to keep the cli as simple as possible.
> Let me show you how it works.

## `Decoding SCTE-35` 
* the cli can __decode SCTE-35__ from __MPEGTS Streams, Base64, Hex, HLS, JSON, Xml, and Xml+Bin__ formats.
* Most __input__ formats are __auto-detected__ 

### Base64 

```asm
fu '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU='
```

### Hex

```smalltalk
fu '0xfc302c00000003289800fff00a05000000017f5f999901010011020f43554549000000007f8001003500002d974195'
```

### HLS

```lua
fu hls https://example.com/master.m3u8
```

### Json

```lua
cat json.json | fu
```
### Xml

```lua
fu  < xml.xml
```
### Xml+bin

```lua
fu < xmlbin.xml
```
___
## `Output`

* Base64, Bytes, Hex, Json, Int, Xml, or Xml+bin can be specified as output.
* default __output is json__
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

### __base64__
```lua
fu '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' base64
```
* _output_
```lua
/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=
```
### __bytes__
```lua
fu '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' bytes
```
* _output_
```lua
b'\xfc0,\x00\x00\x00\x03(\x98\x00\xff\xf0\n\x05\x00\x00\x00\x01\x7f_\x99\x99\x01\x01\x00\x11\x02\x0fCUEI\x00\x00\x00\x00\x7f\x80\x01\x005\x00\x00-\x97A\x95'
```
### __hex__
```lua
fu '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' hex
```
* _output_
```lua
0xfc302c00000003289800fff00a05000000017f5f999901010011020f43554549000000007f8001003500002d974195
```
### __int__
```lua
fu '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' int
```
* _output_
```lua
151622312799635094191794191736756941723013293850254190245706580675544251579467254651746556435953373552591284683157
```
### __xml__
```lua
fu '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' xml
```
* _output_
```xml
<scte35:SpliceInfoSection xmlns:scte35="https://scte.org/schemas/35"  ptsAdjustment="207000" protocolVersion="0" sapType="3" tier="4095">
   <scte35:SpliceInsert spliceEventId="1" spliceEventCancelIndicator="false" spliceImmediateFlag="true" eventIdComplianceFlag="true" availNum="1" availsExpected="1" outOfNetworkIndicator="false" uniqueProgramId="39321"/>
   <!-- Provider Placement Opportunity End -->
   <scte35:SegmentationDescriptor segmentationEventId="0" segmentationEventCancelIndicator="false" segmentationEventIdComplianceIndicator="true" segmentationTypeId="53" segmentNum="0" segmentsExpected="0">
      <scte35:DeliveryRestrictions webDeliveryAllowedFlag="false" noRegionalBlackoutFlag="false" archiveAllowedFlag="false" deviceRestrictions="0"/>
      <!-- Type 0x01 is deprecated. Use type 0x0C, MPU. -->
      <scte35:SegmentationUpid segmentationUpidType="1" segmentationUpidFormat="hexbinary"/>
   </scte35:SegmentationDescriptor>
</scte35:SpliceInfoSection>
```
### __xml+bin__
```xml
fu '/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=' xmlbin
```
* _output_
```xml
<scte35:Signal xmlns:scte35="https://scte.org/schemas/35">
   <scte35:Binary>/DAsAAAAAyiYAP/wCgUAAAABf1+ZmQEBABECD0NVRUkAAAAAf4ABADUAAC2XQZU=</scte35:Binary>
</scte35:Signal>
```
___

## `File and Network Protocols`

### __File__
  
```lua
fu video.ts
```

### __Http(s)__
  
```lua
fu https://example.com/master.m3u8
```

### __Multicast__

```lua
fu udp://@235.35.3.5:9999
```

### __stdin__

```lua
cat video.ts | fu
```

### __Udp Unicast__

```lua
fu udp://10.0.0.7:5555
```
___

## HLS



