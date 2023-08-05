from collections import UserDict, Mapping
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
        res = self.data
        for k in key:
            if k not in res:
                return None
            res = res[ k ]
        return res

    def update( *args, **kwargs ):
        self, other, *args = args
        for k, v in other.items():
            if k in self.data and isinstance( v, Mapping ):
                self[ k ].update( v )
            else:
                self[ k ] = v
        return self

    def copy( self ):
        return CombinationDict( self.separator, self.data )

    def __getitem__( self, key ):
        return self._locate( self.key_pattern.split( key ) )

    def __setitem__( self, key, value ):
        key = self.key_pattern.split( key )
        res = self._locate( key[ :-1 ] )
        res[ key[ -1 ] ] = value

    def __contains__( self, key ):
        return self._locate( self.key_pattern.split( key ) )