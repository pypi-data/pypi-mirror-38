from collections import UserDict
from collections.abc import Mapping
import re


class CombinationDict( UserDict ):
    """ A Mapping object with convenient shorthand for references nested keys

        Behaves almost identically to a dictionary, with the added convenience
        that nested dictionary keys can be referenced in a single string key,
        with nesting level specified by the separator char.
        e.g., with d = CombinationDict( '.', { ... } ), you can reference keys
        like this:

         dict[ 'a' ][ 'b' ][ 'c' ]  => dict[ 'a.b.c' ]

        You can also escape the separator (it's matched against a regex, so
        escaping is with the back-slash (r'\')) to force a key to be used literally
    """
    def __init__( self, separator, content=None, **kwargs ):
        self.separator = separator
        self.key_pattern = re.compile( rf'(?<!\\){re.escape(self.separator)}' )
        UserDict.__init__( self, content, **kwargs )

    def _locate( self, key ):
        res = self
        for k in key:
            if k not in res.data:
                raise IndexError
            res = res.data[ k ]
        return res

    def update( *args, **kwargs ):
        self, other, *args = args
        if not isinstance( other, Mapping ):
            other = dict( other )
        for k, v in other.items():
            if k in self.data and isinstance( v, Mapping ):
                if isinstance( self[ k ], Mapping ):
                    self[ k ].update( v )
                else:
                    self[ k ] = CombinationDict( self.separator, v )
            else:
                self[ k ] = v
        return self

    def copy( self ):
        return CombinationDict( self.separator, self.data )

    def __getitem__( self, key ):
        item = self._locate( self.key_pattern.split( key ) )
        return item

    def __setitem__( self, key, value ):
        key = self.key_pattern.split( key )
        res = self._locate( key[ :-1 ] )
        if isinstance( value, Mapping ):
            value = CombinationDict( self.separator, value )
        res.data[ key[ -1 ] ] = value
        setattr( res, key[ -1 ], value )

    def __contains__( self, key ):
        try:
            return self._locate( self.key_pattern.split( key ) )
        except IndexError:
            return False
