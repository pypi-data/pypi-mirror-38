## SimpleFixedWidth ##
_A simple and very lightweight library for working with fixed width files._

#### Fixed_Width_Spec ####
class **Field** 

Signature 

` Field(number: int, name: int, string: bool, size:int)`

*  number: int (Positional identifier for the field)
*  name: str (Name of the field)
*  string: bool (Indicates if the field is a string, if false it is numeric)
*  size: int (Length of the field)
  
Example 

`Field(5, 'Name', True, 30)`

class **RecordType** 

Signature 

` RecordType(name="", fields=[])`

*  name: str (Name of the RecordType, if you have more than one)
*  fields: list  (List of fields for the specification tied to the RecordType)
*  field_widths: tuple (Returns tuple of the widths from the fields)
*  field_names: list (Returns list of the field names)

#### Fixed_Width_Record ####
function **get_fields**
    
Slices a string 's' in segments 'args' wide. Negative widths represent ignored padding fields.

**Parameters**
*  s: string
*  args: list of widths for the string, negative numbers are skipped

**Returns** string 's' in a list, minus the skipped fields

function **get_line**

Takes a string and extracts the record identifier if it exists.  

**Parameters**

*  string (String to be sliced into a list of fields)
*  rec_type_start=-1 (If the string contains a record identifier, this will start to parse it out)
*  rec_type_end=-1 (If the string contains a record identifier, this will end to parse it out)

**Returns** 
Tuple of the record identifier and the string it was in.