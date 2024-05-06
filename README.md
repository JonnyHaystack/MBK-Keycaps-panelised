# Panelised MBK Choc Keycaps

## Overview

I wrote the script in [src](src/keycap.py) using [build123d](https://github.com/gumyr/build123d) in order to connect multiple copies of an arbitrary model together via a "sprue" structure that allows them to be 3D printed together and easily separated.
This is useful for ordering small items from services like JLCPCB with a minimum price per part, or constraints on minimum part size.
The script can be modified to import a different STEP model, and you simply need to adjust the location of the `RigidJoint` on the imported model [here](https://github.com/JonnyHaystack/MBK-Keycaps-panelised/blob/master/src/keycap.py#L23).
You should be able to leave pretty much everything as it is.

I recommend using [vscode-ocp-cad-viewer](https://github.com/bernhard-42/vscode-ocp-cad-viewer) for working on build123d projects like this. It is possible to use this [template repository](https://github.com/JonnyHaystack/codespaces-build123d) I set up to do this in your browser using GitHub Codespaces.

## License and attribution

The original choc keycap model included/imported here comes from [here](https://www.thingiverse.com/thing:4564253), designed by [darryldh](https://www.thingiverse.com/darryldh).

The original files are released under the license [Creative Commons - Attribution - Non-Commercial](https://creativecommons.org/licenses/by-nc/4.0/), so the output files in this repository or any other files generated from that MBK keycap model must be used under the terms of that license.
