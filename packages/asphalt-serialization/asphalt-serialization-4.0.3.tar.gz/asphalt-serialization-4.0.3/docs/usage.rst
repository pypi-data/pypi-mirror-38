Using serializers
=================

Using serializers is quite straightforward::

    async def handler(ctx):
        serialized = ctx.json.serialize({'foo': 'example JSON object'})
        original = ctx.json.deserialize(payload)

This example assumes a configuration where a JSON serializer is present as ``ctx.json``.

To see what Python types can be serialized by every serializer, consult the documentation of the
abstract :class:`~asphalt.serialization.api.Serializer` class.


Registering custom types with serializers
-----------------------------------------

An application may sometimes need to send over the wire instances of classes that are not normally
handled by the chosen serializer. In order to do that, a process called *marshalling* is used to
reduce the object to something the serializer can natively handle. Conversely, the process
of restoring the original object from a natively serializable object is called *unmarshalling*.

The ``pickle`` serializer obtains the serializable state of an object from the ``__dict__``
attribute, or alternatively, calls its ``__getstate__()`` method. Conversely, when deserializing it
creates a new object using ``__new__()`` and either sets its ``__dict__`` or calls its
``__setstate__`` method. While this is convenient, pickle has an important drawback that limits
its usefulness. Pickle's deserializer automatically imports arbitrary modules and can trivially be
made to execute any arbitrary code by maliciously constructing the datastream.

A better solution is to use one of the ``cbor``, ``msgpack`` or ``json`` serializers and register
each type intended for serialization using
:meth:`~asphalt.serialization.api.CustomizableSerializer.register_custom_type`. This method lets
the user register marshalling/unmarshalling functions that are called whenever the serializer
encounters an instance of the registered type, or when the deserializer needs to reconstitute an
object of that type using the state object previously returned by the marshaller callback.

The default marshalling callback mimics pickle's behavior by returning the ``__dict__`` of an
object or the return value of its ``__getstate__()`` method, if available. Likewise, the default
unmarshalling callback either updates the ``__dict__`` attribute of the uninitialized instance, or
calls its ``__setstate__()`` method, if available, with the state object.

The vast majority of classes are directly compatible with the default marshaller and unmarshaller
so registering them is quite straightforward::

    from asphalt.serialization.serializers.json import JSONSerializer


    class User:
        def __init__(self, name, email, password):
            self.name = name
            self.email = email
            self.password = password

    serializer = JSONSerializer()
    serializer.register_custom_type(User)

If the class defines ``__slots__`` or requires custom marshalling/unmarshalling logic, the easiest
way is to implement ``__getstate__`` and/or ``__setstate__`` in the class::

    class User:
        def __init__(self, name, email, password):
            self.name = name
            self.email = email
            self.password = password

        def __getstate__(self):
            # Omit the "password" attribute
            dict_copy = self.__dict__.copy()
            del dict_copy['password']
            return dict_copy

        def __setstate__(self, state):
            state['password'] = None
            self.__dict__.update(state)

    serializer = JSONSerializer()
    serializer.register_custom_type(User)

If you are unable to modify the class itself, you can instead use standalone functions for that::

    def marshal_user(user):
        # Omit the "password" attribute
        dict_copy = user.__dict__.copy()
        del dict_copy['password']
        return dict_copy


    def unmarshal_user(user, state):
        state['password'] = None
        user.__dict__.update(state)

    serializer.register_custom_type(User, marshal_user, unmarshal_user)

The callbacks can be a natural part of the class too if you want::

    class User:
        def __init__(self, name, email, password):
            self.name = name
            self.email = email
            self.password = password

        def marshal(self):
            # Omit the "password" attribute
            dict_copy = self.__dict__.copy()
            del dict_copy['password']
            return dict_copy

        def unmarshal(self, state):
            state['password'] = None
            self.__dict__.update(state)

    serializer.register_custom_type(User, User.marshal, User.unmarshal)

.. hint:: If a component depends on the ability to register custom types, it can request a resource
 of type :class:`~asphalt.serialization.api.CustomizableSerializer` instead of
 :class:`~asphalt.serialization.api.Serializer`.

Disabling the default wrapping of marshalled custom types
---------------------------------------------------------

When you register a custom type with a serializer, it by default wraps its marshalled instances
during serialization in a way specific to each serializer in order to include the type name
necessary for automatic deserialization. For example, the ``json`` serializer wraps the state of a
marshalled object in a JSON object like
``{"__type__": "MyTypeName", "state": {"some_attribute": "some_value"}}``.

In situations where you need to serialize objects for a recipient that does not understand this
special wrapping, you can forego the wrapping step by passing the ``wrap_state=False`` option to
the serializer. Doing so will cause the naked state object to be directly serialized.
Of course, this will disable the automatic deserialization, since the required metadata is no
longer available.

Serializing built-in custom types
---------------------------------

If you need to (de)serialize types that have mandatory arguments for their ``__new__()`` method,
you will need to supply a specialized unmarshaller callback that returns a newly created instance
of the target class. Likewise, if the class has neither a ``__dict__`` or a ``__getstate__()``
method, a specialized marshaller callback is required.

For example, to successfully marshal instances of :class:`datetime.timedelta`, you could use the
following (un)marshalling callbacks::

    from datetime import timedelta


    def marshal_timedelta(td):
        return td.total_seconds()


    def unmarshal_timedelta(seconds):
        return timedelta(seconds=seconds)

    serializer.register_custom_type(timedelta, marshal_timedelta, unmarshal_timedelta)

As usual, so long as the marshaller and unmarshaller callbacks agree on the format of the state
object, it can be anything natively serializable.
