# ArgResolver v0.3.2

[![Build Status](https://travis-ci.org/HazardDede/argresolver.svg?branch=master)](https://travis-ci.org/HazardDede/argresolver)

Resolver is a simple decorator for resolving (missing) arguments at runtime.
It performs various tasks from looking up arguments from the environment variable scope to simple service dependency injection.

1\.  [Resolver](#resolver)  
1.1\.  [Environment](#environment)  
1.2\.  [Map](#map)  
1.3\.  [Chain](#chain)  

<a name="resolver"></a>

## 1\. Resolver

<a name="environment"></a>

### 1.1\. Environment

```python
# We inject arguments from the environment variables scope to a simple function
# We use a `prefix` to minimize clashes with other components
# username will have a correponding DB_USERNAME, same for password and database

from argresolver import Environment
from argresolver.utils import modified_environ  # We use it to alter the environment variables

@Environment()
def connect(host, user, password):
    print("Connecting: {user}:{password}@{host}".format(**locals()))

with modified_environ(PASSWORD='my_pass'):
    connect('localhost', 'admin')
# Prints: Connecting: admin:my_pass@localhost
```

```python
# We inject arguments from the environment variables scope 
# to an instance __init__.
# We use a `prefix` to minimize clashes with other components that have a username / password.
# Argument username will have a correponding DB_USERNAME, same for password and database

from argresolver import Environment
from argresolver.utils import modified_environ  # We use it to alter the environment variables

class Connection:
    @Environment(prefix='DB')
    def __init__(self, username, password, database='default'):
        self.username = username
        self.password = password
        self.database = database

    def __str__(self):
        # Hint: In a real world example you won't put your password in here ;-)
        return "Connection(username='{self.username}', password='{self.password}'"\
        ", database='{self.database}')".format(self=self)

with modified_environ(DB_USERNAME='admin', DB_PASSWORD='secret'):
    conn = Connection()
print(str(conn))  # Connection(username='admin', password='secret', database='default')
```

<a name="map"></a>

### 1.2\. Map

```python
# We use the Map resolver to override an argument's default value 
# that is better suited for our needs.

from argresolver import Map

# Let's assume we cannot touch this code...
class Foo:
    def __init__(self, arg1, arg2='I_dont_like_this_default'):
        self.arg1 = arg1
        self.arg2 = arg2

    def __str__(self):
        return "Foo(arg1='{self.arg1}', arg2='{self.arg2}')".format(self=self)

# But we can alter the class and wrap a resolver around the class __init__ 
Foo.__init__ = Map(dict(arg2="better_default"), default_override=True)(Foo.__init__)

foo = Foo("this is arg1")
print(str(foo))  # Foo(arg1='this is arg1', arg2='better_default')
```

<a name="chain"></a>

### 1.3\. Chain

```python
# We do some automatic dependency injection with fallback

from argresolver import Chain, Const, Map

inject = Chain(
    Map(dict(service1="Service1", service2="Service2")), 
    Const("Fallback Service")
)

class Orchestration:
    @inject
    def business_process1(self, service1, service2):
        print("Calling service:", service1)
        print("Calling service:", service2)

    @inject
    def business_process2(self, service1, service3):
        print("Calling service:", service1)
        print("Calling service:", service3)

orchester = Orchestration()
orchester.business_process1()
# Prints:
# Calling service: Service1
# Calling service: Service2

orchester.business_process2()
# Prints:
# Calling service: Service1
# Calling service: Fallback Service
```

