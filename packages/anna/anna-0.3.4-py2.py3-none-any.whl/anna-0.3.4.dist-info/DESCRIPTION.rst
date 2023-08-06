Anna - A Neat configuratioN Auxiliary
=====================================

Anna helps you configure your application by building the bridge between the components of
your application and external configuration sources. It allows you to keep your code short and
flexible yet explicit when it comes to configuration - the necessary tinkering is performed by
the framework.

Anna contains lots of "in-place" documentation aka doc strings so make sure you check out those
too ("``help`` yourself")!


80 seconds to Anna
------------------

Anna is all about *parameters* and *configuration sources*. You declare parameters as part of
your application (on a class for example) and specify their values in a configuration source.
All you're left to do with then is to point your application to the configuration source and
let the framework do its job.

An example is worth a thousand words
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Say we want to build an application that deals with vehicles. I'm into cars so the first thing
I'll do is make sure we get one of those::

    >>> class Car:
    ...     def __init__(self, brand, model):
    ...         self._brand = brand
    ...         self._model = model
    >>>
    >>> your_car = Car('Your favorite brand', 'The hottest model')

Great! We let the user specify the car's ``brand`` and ``model`` and return him a brand new car!

Now we're using ``anna`` for declaring the parameters::

    >>> from anna import Configurable, parametrize, String, JSONAdaptor
    >>>
    >>> @parametrize(
    ...     String('Brand'),
    ...     String('Model')
    ... )
    ... class Car(Configurable):
    ...     def __init__(self, config):
    ...         super(Car, self).__init__(config)
    >>>
    >>> your_car = Car(JSONAdaptor('the_file_where_you_specified_your_favorite_car.json'))

The corresponding json file would look like this::

    {
        "Car/Parameters/Brand": "Your favorite brand",
        "Car/Parameters/Model": "The hottest model",
    }

It's a bit more to type but this comes at a few advantages:

* We can specify the type of the parameter and ``anna`` will handle the necessary conversions
  for us; ``anna`` ships with plenty of parameter types so there's much more to it than just
  strings!
* If we change your mind later on and want to add another parameter, say for example the color
  of the car, it's as easy as declaring a new parameter ``String('Color')`` and setting it as
  a class attribute; all the user needs to do is to specify the corresponding value in
  the configuration source. Note that there's no need to change any interfaces/signatures or
  other intermediate components which carry the user input to the receiving class; all it expects
  is a configuration adaptor which points to the configuration source.
* The configuration source can host parameters for more than only one component, meaning again
  that we don't need to modify intermediate parts when adding new components to our application;
  all we need to do is provide the configuration adaptor.


Five minutes hands-on
---------------------

The 80 seconds intro piqued your curiosity? Great! So let's move on! For the following
considerations we'll pick up the example from above and elaborate on it more thoroughly.

Let's start with a quick Q/A session
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**So what happened when using the decorator ``parametrize``?** It received a number of parameters
as arguments which it set as attributes on the receiving class. Field names are deduced from
the parameters names applying CamelCase to _snake_case_with_leading_underscore conversion.
That is ``String('Brand')`` is set as ``Car._brand``.

**All right, but how did the instance receive its values then?** Note that ``Car`` inherits from
``Configurable`` and ``Configurable.__init__`` is where the actual instance configuration happens.
We provided it a configuration adaptor which points to the configuration source (in this case
a local file) and the specific values were extracted from there. Values are set on the instance
using the parameter's field name, that is ``String('Brand')`` will make an instance receive
the corresponding value at ``your_car._brand`` (``Car._brand`` is still the parameter instance).

**Okay, but how did the framework know where to find the values in the configuration source?**
Well there's a bit more going on during the call to ``parametrize`` than is written above.
In addition to setting the parameters on the class it also deduces a configuration path for
each parameter which specifies where to find the corresponding value in the source. The path
consists of a base path and the parameter's name: "<base-path>/<name>" (slashes are used
to delimit path elements). ``parametrize`` tries to get this base path from the receiving class
looking up the attribute ``CONFIG_PATH``. If it has no such attribute or if it's ``None`` then
the base path defaults to "<class-name>/Parameters". However in our example - although we didn't
set the config path explicitly - it was already there because ``Configurable`` uses a custom
metaclass which adds the class attribute ``CONFIG_PATH`` if it's missing or ``None`` using
the same default as above. So if you want to specify a custom path within the source you can do so
by specifying the class attribute ``CONFIG_PATH``.

**_snake_case_with_leading_underscore, not too bad but can I choose custom field names for the parameters too?**
Yes, besides providing a number of parameters as arguments to ``parametrize`` we have the option
to supply it a number of keyword arguments as well which represent field_name / parameter pairs;
the key is the field name and the value is the parameter: ``brand_name=String('Brand')``.

**Now that we declared all those parameters how does the user know what to specify?**
``anna`` provides a decorator ``document_parameters`` which will add all declared parameters to
the component's doc string under a new section. Another option for the user is to retrieve
the declared parameters via ``get_parameters`` (which is inherited from ``Configurable``) and
print their string representations which contain comprehensive information::

    >>> for parameter in Car.get_parameters():
    ...     print(parameter)

Of course documenting the parameters manually is also an option.

Alright so let's get to the code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    >>> from anna import Configurable, parametrize, String, JSONAdaptor
    >>>
    >>> @parametrize(
    ...     String('Model'),
    ...     brand_name=String('Brand')
    ... )
    ... class Car(Configurable):
    ...     CONFIG_PATH = 'Car'
    ...     def __init__(self, config):
    ...         super(Car, self).__init__(config)

Let's first see what information we can get about the parameters::

    >>> for parameter in Car.get_parameters():
    ...     print(parameter)
    ...
    {
        "optional": false,
        "type": "StringParameter",
        "name": "Model",
        "path": "Car"
    }
    {
        "optional": false,
        "type": "StringParameter",
        "name": "Brand",
        "path": "Car"
    }

Note that it prints ``"StringParameter"`` because that's the parameter's actual class,
``String`` is just a shorthand. Let's see what we can get from the doc string::

    >>> print(Car.__doc__)
    None
    >>> from anna import document_parameters
    >>> Car = document_parameters(Car)
    >>> print(Car.__doc__)

        Declared parameters
        -------------------
        (configuration path: Car)

        Brand : String
        Model : String


Now that we know what we need to specify let's get us a car! The ``JSONAdaptor`` can also be
initialized with a ``dict`` as root element, so we're just creating our configuration on the fly::

    >>> back_to_the_future = JSONAdaptor(root={
    ...     'Car/Brand': 'DeLorean',
    ...     'Car/Model': 'DMC-12',
    ... })
    >>> doc_browns_car = Car(back_to_the_future)
    >>> doc_browns_car.brand_name  # Access via our custom field name.
    'DeLorean'
    >>> doc_browns_car._model  # Access via the automatically chosen field name.
    'DMC-12'

Creating another car is as easy as providing another configuration source::

    >>> mr_bonds_car = Car(JSONAdaptor(root={
    ...     'Car/Brand': 'Aston Martin',
    ...     'Car/Model': 'DB5',
    ... }))

Let's assume we want more information about the brand than just its name. We have nicely stored
all information in a database::

    >>> database = {
    ... 'DeLorean': {
    ...     'name': 'DeLorean',
    ...     'founded in': 1975,
    ...     'founded by': 'John DeLorean',
    ... },
    ... 'Aston Martin': {
    ...     'name': 'Aston Martin',
    ...     'founded in': 1913,
    ...     'founded by': 'Lionel Martin, Robert Bamford',
    ... }}

We also have a database access function which we can use to load stuff from the database::

    >>> def load_from_database(key):
    ...     return database[key]

To load this database information instead of just the brand's name we only have to modify
the ``Car`` class to declare a new parameter: ``ActionParameter`` (or ``Action``).
An ``ActionParameter`` wraps another parameter and let's us specify an action which is applied to
the parameter's value when it's loaded. For our case that is::

    >>> from anna import ActionParameter
    >>> Car.brand = ActionParameter(String('Brand'), load_from_database)
    >>> doc_browns_car = Car(back_to_the_future)
    >>> doc_browns_car.brand
    {'founded by': 'John DeLorean', 'name': 'DeLorean', 'founded in': 1975}
    >>> doc_browns_car.brand_name
    'DeLorean'

Note that we didn't need to provide a new configuration source as the new ``brand`` parameter is
based on the brand name which is already present.

Say we also want to obtain the year in which the model was first produced and we have a function
for exactly that purpose however it requires the brand name and model name as one string::

    >>> def first_produced_in(brand_and_model):
    ...     return {'DeLorean DMC-12': 1981, 'Aston Martin DB5': 1963}[brand_and_model]

That's not a problem because an ``ActionParameter`` type lets us combine multiple parameters::

    >>> Car.first_produced_in = ActionParameter(
    ... String('Brand'),
    ... lambda brand, model: first_produced_in('%s %s' % (brand, model)),
    ... depends_on=('Model',))

Other existing parameters, specified either by name of by reference via the keyword argument
``depends_on``, are passed as additional arguments to the given action.

In the above example we declared parameters on a class using ``parametrize`` but you could as well
use parameter instances independently and load their values via ``load_from_configuration`` which
expects a configuration adaptor as well as a configuration path which localizes the parameter's
value. You also have the option to provide a specification directly via
``load_from_representation``. This functions expects the specification as a unicode string and
additional (meta) data as a ``dict`` (a unit for ``PhysicalQuantities`` for example).

This introduction was meant to demonstrate the basic principles but there's much more to ``anna``
(especially when it comes to parameter types)! So make sure to check out also the other parts
of the docs!


Parameter types
---------------

A great variety of parameter types are here at your disposal:

* ``Bool``
* ``Integer``
* ``String``
* ``Number``
* ``Vector``
* ``Duplet``
* ``Triplet``
* ``Tuple``
* ``PhysicalQuantity``
* ``Action``
* ``Choice``
* ``Group``
* ``ComplementaryGroup``
* ``SubstitutionGroup``


Configuration adaptors
----------------------

Two adaptor types are provided:

* ``XMLAdaptor`` for connecting to xml files.
* ``JSONAdaptor`` for connecting to json files (following some additional conventions).


Generating configuration files
------------------------------

Configuration files can of course be created manually however ``anna`` also ships with a ``PyQt``
frontend that can be integrated into custom applications. The frontend provides input forms for
all parameter types as well as for whole parametrized classes together with convenience methods for
turning the forms' values into configuration adaptor instances which in turn can be dumped to
files. Both PyQt4 and PyQt5 are supported. See ``anna.frontends.qt``.


