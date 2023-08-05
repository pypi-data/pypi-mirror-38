# Kea / script templates






## Template layout

A kea/template is a plain file that can be read and parsed by kea, and
subsequently executed. Arguments are provided on the commandline.

Templates typically executable and start with a shebang:

    #!/usr/bin/env kea

Followed by the actual script, which can be anything that is in a normal script. For example:

    #!/usr/bin/env kea
    #!/bin/bash

    echo "Hello World!"

or:

    #!/usr/bin/env kea
    #!/usr/bin/env python

    print("Hello World!")


Both of which Kea will take and execute as if normal bash/python scripts.
