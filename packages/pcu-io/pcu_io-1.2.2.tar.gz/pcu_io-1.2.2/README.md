# pcu_io (IO management for PCU project)

IO management for PCU project.
From the path of a file (PDF or JSON), parse it in order to get its textual content.

----

[Check PCU project][pcu].

[pcu]: https://github.com/zevio/pcu_core

----

## Usage in another project

If you wish to import this module in another Python project, please install it :

`pip install pcu-io`

Then, add this import line at the beginning of your Python file :

`from pcu_io import pcu_io`

You can now use pcu_io's functions, for example :

`pcu_io.getEquivalentTextfile(path/to/json/or/pdf/file)`

## Test

To test your installation, go to pcu_io/ directory and execute the Makefile with the following command line : 

`make test`
