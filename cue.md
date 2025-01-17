# Help on class Cue in module threefive3.cue


```py3

class Cue(threefive3.base.SCTE35Base)
 |  Cue(data=None, packet_data=None)
 |  
 |  The threefive3.Cue class handles parsing
 |  SCTE 35 message strings.
 |  Example usage:
 |  
 |  >>>> import threefive3
 |  >>>> Base64 = "/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g="
 |  >>>> cue = threefive3.Cue(Base64)
 |  >>>> cue.show()
 |  
 |  * A cue instance can be initialized with
 |   Base64, Bytes, Hex, Int, Json, Xml, or Xml+binary data.
 |  
 |  * Instance variables can be accessed via dot notation.
 |  
 |  >>>> cue.command
 |  {'command_length': 5, 'name': 'Time Signal', 'time_specified_flag': True,
 |  'pts_time': 21695.740089}
 |  
 |  >>>> cue.command.pts_time
 |  21695.740089
 |  
 |  Method resolution order:
 |      Cue
 |      threefive3.base.SCTE35Base
 |      builtins.object
 ```  
 * Methods you'll use often:
```py3
 |  
 |  __init__(self, data=None, packet_data=None)
 |      data may be packet bites or encoded string
 |      packet_data is a instance passed from a Stream instance
 | 
 |  base64(self)
 |      base64 Cue.base64() converts SCTE35 data
 |      to a base64 encoded string.
 |  
 |  bytes(self)
 |      get_bytes returns Cue.bites
 |  
 |  hex(self)
 |      hex returns self.bites as
 |      a hex string
 |  
 |  int(self)
 |      int returns self.bites as an int.
 |   
 |  xml(self, ns='scte35')
 |      xml returns a threefive3.Node instance
 |      which can be edited as needed or printed.
 |      xmlbin
 |  
 |  xmlbin(self, ns='scte35')
 |      xml returns a threefive3.Node instance
 |      which can be edited as needed or printed.
 |      xmlbin
 |
 |  get(self)
 |      Cue.get returns the SCTE-35 Cue
 |      data as a dict of dicts.
 |  
 |  get_descriptors(self)
 |      Cue.get_descriptors returns a list of
 |      SCTE 35 splice descriptors as dicts.
 |
```
* Methods available but rarely needed
```py3

  load(self, gonzo)
 |      Cue.load loads SCTE35 data for encoding.
 |      gonzo is a dict or json
 |      with any or all of these keys
 |      gonzo = {
 |          'info_section': {dict} ,
 |          'command': {dict},
 |          'descriptors': [list of {dicts}],
 |          }
 |      
 |      * load doesn't need to be called directly
 |        unless you initialize a Cue without data.
 |  
 |  mk_info_section(self, bites)
 |      Cue.mk_info_section parses the
 |      Splice Info Section
 |      of a SCTE35 cue.

 decode(self)
 |      Cue.decode() parses for SCTE35 data
 |      
 |      * decode doesn't need to be called directly
 |         unless you initialize a Cue without data.
 |  
 |  encode(self)
:     encode is an alias for base64
 | 
 |  ----------------------------------------------------------------------
 |  Static methods defined here:
 |  
 |  fix_bad_b64(data)
 |      fix_bad_b64 fixes bad padding on Base64
 |  
```
### Cue, Stream, All Splice Commands and all Splice Descriptors are subclassed from SCTE35Base

* Methods inherited from threefive3.base.SCTE35Base:
```py3 
 |  has(self, what)
 |      has runs hasattr with self and what
 ___
 use like:

    cue=Cue(data)
    cue.command.has("pts_time")

    returns  True if cue.commnd has the pts_tme var set
    returns False if not 
___
 |  hasis(self, what)
 |      hasis  obj "has" a what and what "is" returned.
---
use like:

    cue=Cue(data)
    pts = cue.command.hasis('pts_time')
    print(pts)
    10736.127982
---
 |  json(self)
 |      json returns self as kv_clean'ed json
 |  
 |  kv_clean(self)
 |      kv_clean recursively removes items
 |      from a dict if the value is None.
 |  
 |  show(self)
 |      show prints self as json to stderr (2)
 |  


* Static Methods inherited from SCTE35Base
```py3
 |  
 |  as_90k(int_time)
 |      ticks to 90k timestamps
 |  
 |  as_hms(secs_of_time)
 |      as_hms converts timestamp to
 |      00:00:00.000 format
 |  
 |  as_ticks(float_time)
 |      90k timestamps to ticks
 |  
 |  fix_hex(hexed)
 |      fix_hex adds padded zero if needed for byte conversion.
 |  
 |  idxsplit(gonzo, sep)
 |      idxsplit is like split but you keep
 |      the sep
 |      example:
 |              >>> idxsplit('123456789',4)
 |              >>>'456789'

```
