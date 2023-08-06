from typing import Optional, Union, List

import neocommand.neocsv.constants
from mhelper import SwitchError, array_helper, MEnum, exception_helper
from neocommand.neocsv.filenames import NcvEntitySpec, NcvFilename
from neocommand.neocsv.types import NeoType


class ENcvSpecial( MEnum ):
    NONE = 0
    UID = 1
    START = 2
    END = 3


class NcvHeader:
    """
    Represents a header (column) of a NeoCsv file.
    
    Access:
        .name               - to get the name (fixed). This is how we see it.
        .decorated_name()   - to get the name, type and label (if required). This is what is actually written to the file.
        
    Use:
        .parse(...)         - to interpret existing
        .from_value(...)    - to create new
    
    The supported column types are:
        * int, long, float, double, boolean, byte, short, char, string
        * And lists thereof
    """
    
    
    def __init__( self, name: Optional[str], type_: Optional[NeoType], special: ENcvSpecial, type_label: Optional[str] = None ):
        """
        CONSTRUCTOR
        :param name: Name of the header
        :param type_: Type of the header (must be a neotype, or NoneType, which will be converted to the most restrictive type "bool")
        """
        if special == ENcvSpecial.NONE:
            if name is None:
                raise ValueError( "The `name` of this NcvHeader is invalid. The name cannot be `None` when the header is not marked as having a special case handler." )
            
            if type_ is None:
                raise ValueError( "The `type_` of this NcvHeader, which has the name «{}», is invalid - the type cannot be `None` when the header is not marked as having a special case handler.".format(name) )
        
        if name:
            if any( x in name for x in ":()" ):
                raise ValueError( "Invalid name for a NcvHeader: «{}».".format( name ) )
        
        self.__name: str = name
        self.__type: NeoType = type_
        self.__special = special
        self.__type_label = type_label
    
    
    @property
    def is_special( self ):
        return not self.is_regular
    
    
    @property
    def is_regular( self ):
        return self.__special == ENcvSpecial.NONE
    
    
    @property
    def type_label( self ):
        return self.__type_label
    
    
    @property
    def name( self ) -> str:
        """
        Obtains the name of this column (with no type decoration)
        """
        return self.__name
    
    
    @property
    def type( self ) -> NeoType:
        """
        Obtains the `NeoType` of this column.
        """
        if self.is_special:
            raise ValueError( "Cannot get `type` from a `NcvHeader.__special == {}` because it doesn't make sense.".format( self.__special ) )
        
        return self.__type
    
    
    @property
    def special( self ) -> ENcvSpecial:
        """
        Obtains any special status of this column.
        """
        return self.__special
    
    
    def __repr__( self ):
        """
        String representation of this column, for debugging.
        """
        if self.__special == ENcvSpecial.NONE:
            return "NcvHeader({} : {})".format( self.__name, self.__type.get_id() )
        else:
            return "NcvHeader(special = {})".format( self.__special )
    
    
    def decorated_name( self, entity: NcvEntitySpec ) -> str:
        """
        Gets the fully decorated column name, including name and type
        """
        exception_helper.safe_cast( "entity", entity, NcvEntitySpec )
        
        if self.__special == ENcvSpecial.UID:
            if entity.is_edge:
                raise ValueError( "Column is of `UID` type but the entity provided is an EDGE." )
            
            return neocommand.neocsv.constants.PRIMARY_KEY_DECORATED_NAME + "(" + entity.label + ")"
        elif self.__special == ENcvSpecial.START:
            if not entity.is_edge:
                raise ValueError( "Column is of `START` type but the entity provided is not an EDGE." )
            
            return neocommand.neocsv.constants.NEO4J_START_ID_SUFFIX + "(" + entity.start_label + ")"
        elif self.__special == ENcvSpecial.END:
            if not entity.is_edge:
                raise ValueError( "Column is of `END` type but the entity provided is not an EDGE." )
            
            return neocommand.neocsv.constants.NEO4J_END_ID_SUFFIX + "(" + entity.end_label + ")"
        elif self.__special == ENcvSpecial.NONE:
            return self.get_basic_decorated_name( self.__name, self.__type )
        else:
            raise SwitchError( "special", self.__special )
    
    
    @classmethod
    def get_basic_decorated_name( cls, name: str, type: NeoType ):
        assert isinstance( type, NeoType )
        return name + ":" + type.neo4j_name
    
    
    def encompass_value( self, value: object ) -> bool:
        """
        Given an existing type and a value, returns the type that would encompass them both the existing data and the new data, if read from a CSV
        """
        if self.__special != ENcvSpecial.NONE:
            if not isinstance( value, str ):
                raise ValueError( "A column of special type «{}» only expected a 'str' value, but the value provided is {} {}.".format( self.__special, type( value ), value ) )
            
            return False
        
        # All floats are strings
        # All ints are floats
        # All bools are ints
        # Nothing can be anything
        
        changes = False
        
        if type( value ) == list:
            the_list: List = value
            
            if len( the_list ) == 0:
                return changes
            elif len( the_list ) == 1:
                type_ = type( the_list[0] )
            else:
                type_ = array_helper.list_type( value )
                if not self.__type.is_array:
                    self.__type = self.__type.ARRAY
                    changes = True
        else:
            type_ = type( value )
        
        if type_ is type( None ):
            # Doesn't matter then!
            return changes
        
        if self.__type.NO_ARRAY is NeoType.STR:
            if (value is None) or (type_ in [str, float, int, bool]):
                return changes
        elif self.__type.NO_ARRAY is NeoType.FLOAT:
            if (value is None) or (type_ in [float, int, bool]):
                return changes
            elif type_ is str:
                self.__type = self.__type.to( NeoType.STR )
                return True
        elif self.__type.NO_ARRAY is NeoType.INT:
            if (value is None) or (type_ in [int, bool]):
                return changes
            elif type_ is float:
                self.__type = self.__type.to( NeoType.FLOAT )
                return True
            elif type_ is str:
                self.__type = self.__type.to( NeoType.STR )
                return True
        elif self.__type.NO_ARRAY is NeoType.BOOL:
            if (value is None) or (type_ in [bool]):
                return changes
            if type_ is int:
                self.__type = self.__type.to( NeoType.INT )
                return True
            elif type_ is float:
                self.__type = self.__type.to( NeoType.FLOAT )
                return True
            elif type_ is str:
                self.__type = self.__type.to( NeoType.STR )  # type: NeoType
                return True
        
        raise ValueError( "Cannot work out how to encompass a new value «{}» of type «{}» into the data column «{}» which is of type «{}».".format( value, type_, self.__name, self.__type ) )
    
    
    @classmethod
    def from_decorated_name( cls, file: Optional[NcvFilename], decorated_name: str ) -> "NcvHeader":
        """ 
        Translates a header's decorated name into a NcvHeader object.
        
        :param file: The file we are reading from. Can be `None` but no error checking is then performed.
        :param decorated_name: A decorated name of one of the forms:
        
                                    1. name:type
                                    2. uid:ID
                                    3. uid:ID(node_label)
                                    4. :END_ID
                                    5. :END_ID(end_label)
                                    6. :START_ID 
                                    7. :START_ID(start_label)
                                    
                                Note that forms 2, 4 and 6 are supported so the caller can remain ignorant of the label;
                                when written via `decorated_name`, the label will always be included.
                                
        :except ValueError: Invalid name.
        """
        from neocommand.data import constants

        # Check the format, it should be `name:type`
        if decorated_name.count( ":" ) != 1:
            raise ValueError( "The column name «{}» in the file «{}» isn't a valid NEO4J-style header. The format should be «name:type», but it isn't.".format( decorated_name, file ) )
        
        # Get the name and the type
        name, type_name = decorated_name.split( ":", 1 )
        
        # Get the label, this is part of the type: `name:type(label)`
        if "(" in type_name:
            type_name, label = type_name.split( "(", 1 )  # type: str, str
            
            if ")" not in label:
                raise ValueError( "Invalid decorated name «{}»: Missing parenthesis.".format( decorated_name ) )
            
            label = label.replace( ")", "", 1 ).strip()
        else:
            label = None
        
        if not type_name:
            raise ValueError( "The type name «{}» is invalid in the decorated name «{}».".format( type_name, decorated_name ) )
        
        # Check if we have one of the specials - primary key, start or end id.
        if name == constants.PRIMARY_KEY or type_name == neocommand.neocsv.constants.NEO4J_ID_TYPE:
            # uid:*
            if name != constants.PRIMARY_KEY:
                raise ValueError( "Invalid decorated name «{}»: Name of UID should be «{}», not «{}».".format( decorated_name, constants.PRIMARY_KEY, name ) )
            
            if type_name != neocommand.neocsv.constants.NEO4J_ID_TYPE:
                raise ValueError( "Invalid decorated name «{}»: Type of UID should be «{}», not «{}».".format( decorated_name, neocommand.neocsv.constants.NEO4J_ID_TYPE, type_name ) )
            
            if file is not None and label and label != file.label:
                raise ValueError( "Invalid decorated name «{}»: Label should be the primary key in the file «{}», not «{}».".format( decorated_name, file, label ) )
            
            return NcvHeader( None, None, ENcvSpecial.UID, label )
        elif type_name == neocommand.neocsv.constants.NEO4J_START_ID_TYPE:
            # *:START_ID[(*)]
            if name:
                raise ValueError( "Invalid decorated name «{}»: Name of START_ID should be empty.".format( decorated_name ) )
            
            if file is not None and label and label != file.start_label:
                raise ValueError( "Invalid decorated name «{}»: Label should be the start label in the file «{}», not «{}».".format( decorated_name, file, label ) )
            
            return NcvHeader( None, None, ENcvSpecial.START, label )
        elif type_name == neocommand.neocsv.constants.NEO4J_END_ID_SUFFIX[1:]:
            # *:END_ID[(*)]
            if name:
                raise ValueError( "Invalid decorated name «{}»: Name of END_ID should be empty.".format( decorated_name ) )
            
            if file is not None and label and label != file.end_label:
                raise ValueError( "Invalid decorated name «{}»: Label should be the end label in the file «{}», not «{}».".format( decorated_name, file, label ) )
            
            return NcvHeader( None, None, ENcvSpecial.END, label )
        else:
            if not name:
                raise ValueError( "Invalid decorated name «{}»: Name of should not be blank.".format( decorated_name ) )
            
            if label:
                raise ValueError( "Invalid decorated name «{}»: Label «{}» not expected.".format( decorated_name, label ) )
            
            neo_type = NeoType.from_name( type_name )
            return NcvHeader( name, neo_type, ENcvSpecial.NONE, label )
    
    
    @staticmethod
    def from_value( name: Union[str, ENcvSpecial], value: object ) -> "NcvHeader":
        """
        Given a `name` and `value`, create a suitable `NcvHeader`. 
        :param name:    Name of the header OR a special key
        :param value:   A value to be stored in the column
        :return: A `NcvHeader` object.
        """
        if isinstance( name, ENcvSpecial ):
            if not isinstance( value, str ):
                raise ValueError( "A column of special type «{}» only expected a 'str' value, but the value provided is {} {}.".format( name, type( value ), value ) )
            
            return NcvHeader( None, None, name )
        elif isinstance( name, str ):
            if type( value ) is list:
                the_list = value  # type:List[object]
                if len( the_list ) == 0:
                    return NcvHeader( name, NeoType.BOOL.ARRAY, ENcvSpecial.NONE )
                elif len( the_list ) == 1:
                    return NcvHeader( name, NeoType.from_type( type( the_list[0] ) ).ARRAY, ENcvSpecial.NONE )
                else:
                    return NcvHeader( name, NeoType.from_type( array_helper.list_type( value ) ).ARRAY, ENcvSpecial.NONE )
            else:
                return NcvHeader( name, NeoType.from_type( type( value ) ), ENcvSpecial.NONE )
        else:
            raise SwitchError( "name", name, instance = True )
