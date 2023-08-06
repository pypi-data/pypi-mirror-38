from typing import GenericMeta, Tuple, cast, Any, List, Sequence, Optional, Union, Callable

from mhelper.mannotation.classes import MAnnotation
from mhelper.mannotation.predefined import isUnion, isOptional


_TUnion = type( Union[int, str] )


class AnnotationInspector:
    """
    Class to inspect PEP-484 generics including `MAnnotation` annotations.
    """
    
    
    def __init__( self, annotation: object ):
        """
        CONSTRUCTOR
        :param annotation: `type` to inspect 
        """
        if isinstance( annotation, AnnotationInspector ):
            raise TypeError( "Encompassing an `AnnotationInspector` within an `AnnotationInspector` is probably an error." )
        
        self.value = annotation
    
    
    @classmethod
    def get_type_name( cls, type_: type ):
        return str( cls( type_ ) )
    
    
    def __str__( self ) -> str:
        """
        Returns the underlying type string
        """
        if isinstance( self.value, type ):
            result = self.value.__name__
        elif isinstance( self.value, MAnnotation ):
            result = str( self.value )
        elif hasattr( self.value, "__forward_arg__" ):  # from typing._ForwardRef
            result = getattr( self.value, "__forward_arg__" )
        else:
            result = "*" + str( self.value )
        
        if result.startswith( "typing." ):
            result = result[7:]
        
        if self.is_generic:
            result += "[" + ", ".join( str( AnnotationInspector( x ) ) for x in self.generic_args ) + "]"
        
        return result
    
    
    @property
    def is_generic( self ):
        """
        Returns if this class is a generic (inherits `GenericMeta`).
        """
        return isinstance( self.value, GenericMeta )
    
    
    @property
    def generic_arg( self ) -> object:
        return self.generic_args[0]
    
    
    @property
    def generic_args( self ) -> Tuple[object, ...]:
        """
        If this class is a generic, returns the arguments.
        """
        if not self.is_generic:
            raise ValueError( "Cannot get `generic_args` because this annotation, «{}» is not a generic.".format( self ) )
        
        return cast( Any, self.value ).__args__
    
    
    @property
    def is_mannotation( self ):
        """
        Is this an instance of `MAnnotation`?
        """
        return isinstance( self.value, MAnnotation )
    
    
    def is_mannotation_of( self, parent: MAnnotation ):
        """
        Is this an instance of `MAnnotation`, specifically a `specific_type` derivative?
        """
        if not self.is_mannotation:
            return False
        
        assert isinstance( self.value, MAnnotation )
        
        return self.value.is_derived_from( parent )
    
    
    @property
    def mannotation( self ) -> MAnnotation:
        """
        Returns the MAnnotation object, if this is an MAnnotation, otherwise raises an error.
        
        :except TypeError: Not an MAnnotation.
        """
        if not self.is_mannotation:
            raise TypeError( "«{}» is not an MAnnotation[T].".format( self ) )
        
        return cast( MAnnotation, self.value )
    
    
    @property
    def mannotation_arg( self ):
        """
        If this is an instance of `MAnnotation`, return the underlying type, otherwise, raise an error.
        """
        if not self.is_mannotation:
            raise TypeError( "«{}» is not an MAnnotation[T].".format( self ) )
        
        assert isinstance( self.value, MAnnotation )
        
        if len( self.value.parameters ) >= 2:
            return self.value.parameters[1]
        else:
            return None
    
    
    @property
    def is_generic_list( self ) -> bool:
        """
        Is this a `List[T]`?
        
        (note: this does not include `list` or `List` with no `T`)
        """
        return self.is_generic_u_of_t( List )
    
    
    def is_generic_u_of_t( self, u: type ):
        """
        Is this a generic U[T]?
        """
        return (isinstance( self.value, type )
                and self.is_generic
                and issubclass( cast( type, self.value ), u )
                and self.generic_args)
    
    
    @property
    def is_generic_sequence( self ) -> bool:
        """
        Is this a `Sequence[T]`?
        """
        return self.is_generic_u_of_t( Sequence )
    
    
    @property
    def generic_list_type( self ) -> type:
        """
        Gets the T in List[T]. Otherwise raises `TypeError`.
        """
        if not self.is_generic_list:
            raise TypeError( "«{}» is not a List[T].".format( self ) )
        
        # noinspection PyUnresolvedReferences
        return self.value.__args__[0]
    
    
    @property
    def is_union( self ) -> bool:
        """
        Is this a `Union[T, ...]`?
        Is this a `isUnion[T, ...]`?
        """
        return isinstance( self.value, _TUnion ) or self.is_mannotation_of( isUnion )
    
    
    def is_direct_subclass_of( self, super_class: type ) -> bool:
        """
        Is `self.value` a sub-class of `lower_class`?
        """
        # If BASE and/or DERIVED is not a type then we count only direct equality
        if self.value is super_class:
            return True
        
        if not self.is_type:
            return False
        
        super_inspector = AnnotationInspector( super_class )
        
        if not super_inspector.is_type:
            return False
        
        if super_inspector.is_generic_list:
            super_inspector = AnnotationInspector( list )
        
        if super_inspector.is_union:
            return any( self.is_direct_subclass_of( x ) for x in super_inspector.union_args )
        else:
            try:
                return issubclass( cast( type, self.value ), super_inspector.value )
            except TypeError as ex:
                raise TypeError( "Cannot determine if «{}» is derived from «{}» because `issubclass({}, {})` returned an error.".format( self, super_class, self, super_class ) ) from ex
    
    
    def is_direct_superclass_of( self, sub_class: type ) -> bool:
        """
        Is `lower_class` a sub-class of `self.value`?
        """
        if not self.is_type:
            return False
        
        if self.is_generic_list:
            # Special case for List[T]
            return issubclass( sub_class, list )
        
        try:
            return issubclass( sub_class, cast( type, self.value ) )
        except TypeError as ex:
            raise TypeError( "Cannot determine if «{}» is a base class of «{}» because `issubclass({}, {})` returned an error.".format( self, sub_class, sub_class, self ) ) from ex
    
    
    def is_direct_subclass_of_or_optional( self, super_class: type ):
        """
        Returns if `value_or_optional_value` is a subclass of `upper_class`.
        """
        return AnnotationInspector( self.value_or_optional_value ).is_direct_subclass_of( super_class )
    
    
    def get_direct_subclass( self, super_class: type ) -> Optional[type]:
        """
        This is the same as `is_direct_subclass_of`, but returns the true `type` (`self.value`) if `True`.
        """
        if self.is_direct_subclass_of( super_class ):
            return cast( type, self.value )
    
    
    def get_direct_superclass( self, lower_class: type ) -> Optional[type]:
        """
        This is the same as `is_direct_superclass_of`, but returns the true `type` (`self.value`) if `True`.
        """
        if self.is_direct_superclass_of( lower_class ):
            return cast( type, self.value )
    
    
    def is_indirect_subclass_of( self, super_class: type ) -> bool:
        """
        Is `self.value` a sub-class of `upper_class`, or an annotation enclosing a class that is a sub-class of `upper_class`? 
        """
        return self.get_indirect_subclass( super_class ) is not None
    
    
    def is_indirectly_superclass_of( self, sub_class: type ) -> bool:
        """
        Is `lower_class` a sub-class of `self.value`, or a sub-class of an annotation enclosed within `self.value`?
        """
        return self.get_indirect_superclass( sub_class ) is not None
    
    
    def get_indirect_superclass( self, sub_class: type ) -> Optional[type]:
        """
        This is the same as `is_indirect_subclass_of`, but returns the true `type` that is above `lower_class`.
        """
        return self.__get_indirectly( sub_class, AnnotationInspector.is_direct_superclass_of )
    
    
    def get_indirect_subclass( self, super_class: type ) -> Optional[type]:
        """
        This is the same as `is_indirectly_superclass_of`, but returns the true `type` that iis below `upper_class`.
        """
        return self.__get_indirectly( super_class, AnnotationInspector.is_direct_subclass_of )
    
    
    def __get_indirectly( self, query: type, predicate: "Callable[[AnnotationInspector, type],bool]" ) -> Optional[object]:
        """
        Checks inside all `Unions` and `MAnnotations` until the predicate matches, returning the type (`self.value`) when it does.
        """
        if predicate( self, query ):
            return self.value
        
        if self.is_union:
            for arg in self.union_args:
                arg_type = AnnotationInspector( arg ).__get_indirectly( query, predicate )
                
                if arg_type is not None:
                    return arg_type
        
        if self.is_mannotation:
            annotation_type = AnnotationInspector( self.mannotation_arg ).__get_indirectly( query, predicate )
            
            if annotation_type is not None:
                return annotation_type
        
        return None
    
    
    @property
    def union_args( self ) -> List[type]:
        """
        Returns the list of Union parameters `[...]`.
        """
        if not self.is_union:
            raise TypeError( "«{}» is not a Union[T].".format( self ) )
        
        # noinspection PyUnresolvedReferences
        if self.is_mannotation_of( isUnion ):
            return self.mannotation_arg
        elif self.is_mannotation_of( isOptional ):
            return [self.mannotation_arg]
        else:
            return cast( _TUnion, self.value ).__args__
    
    
    @property
    def is_optional( self ) -> bool:
        """
        If a `Union[T, U]` where `None` in `T`, `U`.
        """
        if self.is_mannotation_of( isOptional ):
            return True
        
        if not self.is_union:
            return False
        
        if len( self.union_args ) == 2 and type( None ) in self.union_args:
            return True
        
        return False
    
    
    @property
    def is_multi_optional( self ) -> bool:
        """
        If a `Union[...]` with `None` in `...`
        """
        if self.is_mannotation_of( isOptional ):
            return True
        
        if not self.is_union:
            return False
        
        if None in self.union_args:
            return True
        
        return False
    
    
    @property
    def optional_types( self ) -> Optional[List[type]]:
        """
        Returns `...` in a `Union[None, ...]`, otherwise raises `TypeError`.
        """
        if self.is_mannotation_of( isOptional ):
            return [self.mannotation_arg]
        
        if not self.is_union:
            raise TypeError( "«{}» is not a Union[T].".format( self ) )
        
        union_params = self.union_args
        
        if type( None ) not in union_params:
            raise TypeError( "«{}» is not a Union[...] with `None` in `...`.".format( self ) )
        
        union_params = list( self.union_args )
        union_params.remove( type( None ) )
        return union_params
    
    
    @property
    def optional_value( self ) -> Optional[object]:
        """
        Returns `T` in a `Union[T, U]` (i.e. an `Optional[T]`) or `isOptional[T]`.
        Otherwise raises `TypeError`.
        """
        t = self.optional_types
        
        if len( t ) == 1:
            return t[0]
        else:
            raise TypeError( "«{}» is not a Union[T, None] (i.e. an Optional[T]).".format( self ) )
    
    
    @property
    def value_or_optional_value( self ) -> Optional[object]:
        """
        If this is an `Optional[T]` or `isOptional[T]`, returns `T`.
        Otherwise returns `value`.
        """
        if self.is_optional:
            return self.optional_value
        else:
            return self.value
    
    
    @property
    def safe_type( self ) -> Optional[type]:
        """
        If this is a `T`, returns `T`, else returns `None`.
        """
        if self.is_type:
            assert isinstance( self.value, type )
            return self.value
        else:
            return None
    
    
    @property
    def is_type( self ):
        """
        Returns if my `type` is an actual `type`, not an annotation object like `Union`.
        """
        return isinstance( self.value, type )
    
    
    @property
    def name( self ):
        """
        Returns the type name
        """
        if not self.is_type:
            raise TypeError( "«{}» is not a <type>.".format( self ) )
        
        return self.value.__name__
    
    
    def is_viable_instance( self, value ):
        """
        Returns `is_viable_subclass` on the value's type.
        """
        if value is None and self.is_optional:
            return True
        
        return self.is_indirectly_superclass_of( type( value ) )
