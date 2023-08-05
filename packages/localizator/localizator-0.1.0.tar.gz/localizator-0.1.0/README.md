# Localizator

Purpose of this simple package is to give easy to use abstractions for localizing your python app. Generally this package was made just for my telegram bots.

## Initialization
Firstly, you have to create localizator object:
```Python
from localizator import Localizator

localizator = Localizator()
```

Also, you could pass `LocalizationsProvider` and default language. LocalizationsProvider is fabric that creates `Localization`s objects by language name.
By default it will use YAML implementation that looks for `*.yaml` files inside `localizations` directory, but you could create your own localizations provider or at least change directory if it's necessary.
 
If you did not change anything in localizator initialization, create directory inside working directory called `localizations` and create file `en.yaml` with example content:
```yaml
foo: bar

extended_foo:
  bar: foo

world: "{} world"
formatting: "Hello, {}!"
named_formatting: "Hello, {world}!"
```  

## Simple use

After that you can start using localizator:

```Python
from localizator import LocalizationDescription
from localizator import Localizator

localizator = Localizator()

print(localizator.get_localization(LocalizationDescription(['foo'])))
print(localizator.get_localization(LocalizationDescription(['extended_foo', 'bar'])))
```

## Describer
Looks not really simple? Yeah, it's, but do not stop here! We have _brand new_ `Describer`. It allows to make your localization really simple, i mean, just look:

```Python
from localizator import LocalizationDescriber
from localizator import Localizator

d = LocalizationDescriber()
localizator = Localizator()

print(localizator.get_localization(d.foo))
print(localizator.get_localization(d.extended_foo.bar))

# And even more!
print(localizator.get_localization(d.formatting("world")))
print(localizator.get_localization(d.named_formatting(world="world")))


# Moar!
print(localizator.get_localization(d.formatting(d.world('breathtaking'))))
```

Also, if you want to highlight your paths to localizations as strings, you could use string:
```Python
print(localizator.get_localization(d('foo')))
print(localizator.get_localization(d('extended_foo.bar')))
``` 
