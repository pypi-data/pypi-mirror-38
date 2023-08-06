import unittest
from enum import Enum
from typing import Union, Optional, List

from mhelper import isOptionList
from stringcoercion import get_default_collection, CoercionError


class AnEnum( Enum ):
    ALPHA = 1
    BETA = 2
    GAMMA = 3


opts = ["ONE", "TWO", "THREE"]
ONEOF = isOptionList(str, lambda: opts)


class MyTestCase( unittest.TestCase ):
    def __test( self, c, type_, text, expected ) -> None:
        if isinstance( expected, type ) and issubclass( expected, Exception ):
            try:
                v = c.coerce( type_, text )
            except Exception as ex:
                v = type( ex )
        else:
            v = c.coerce( type_, text )
        
        if v != expected:
            self.fail( "value invalid, expected {} but got {}".format( repr( expected ), repr( v ) ) )
        
        if not type( v ) is type( expected ):
            self.fail( "type invalid, expected {} but got {}".format( repr( type( expected ) ), repr( type( v ) ) ) )
    
    
    def test_one( self ) -> None:
        c = get_default_collection()
        
        self.__test( c, List[bool], "True,1,Yes,False,0,No", [True, True, True, False, False, False] )
        self.__test( c, Optional[bool], "none", None )
        self.__test( c, int, "1", 1 )
        self.__test( c, Union[int, float], "1", 1 )
        self.__test( c, Union[int, float], "1.0", 1.0 )
        self.__test( c, Union[float, int], "1", 1.0 )
        self.__test( c, Union[None, bool], "1", True )
        self.__test( c, Union[None, bool], "none", None )
        self.__test( c, Optional[bool], "True", True )
        self.__test( c, Union[bool, str], "beans", "beans" )
        self.__test( c, Union[bool, str], "yes", True )
        self.__test( c, List[Union[bool, str]], "True,1,Yes,False,0,No,Beans", [True, True, True, False, False, False, "Beans"] )
        self.__test( c, AnEnum, "BETA", AnEnum.BETA )
        self.__test( c, ONEOF, "TWO", "TWO" )
        self.__test( c, ONEOF, "FIVE", CoercionError )


if __name__ == '__main__':
    unittest.main()
