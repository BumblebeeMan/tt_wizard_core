# Welcome to TT_WIZARD_CORE!

This projects provides an operating system independent backend to download and manage *.gme-files / audio files for the TipToi pen sold by Ravensburger. By removing the hassle to deal with file versioning and download servers, it especially enables the creation of tools for operating systems that are currently not officially supported by the manufacturer itself (like Linux). **TT_WIZARD_CORE** only uses the official servers (i.e. hosted by the manufacturer) to download any media files! 

## Following operations are currently supported:
- Searching the names of all currently published TipToi media for a keyword (e.g. "puzzle" to get all puzzles listed).
- Picking and downloading selected media from the search results above.
- Auto detect of pen mount point (tests ongoing)

## Planned features
- Checking whether an already downloaded media file needs an update or not. (Postponed to next version.)
- Auto update of media files that are already loaded to the TipToi pen. (Postponed to next version.)
- Update dependencies: Test / expand compatability with older versions

## Installation of released version

Use pip to install:

```python
pip install tt_wizard_core
```
 
## Usage
See example included in "ExampleApp.py".

# Disclaimer and Trademark Notice

NOTE: This package is not verified by, affiliated with, or supported by Ravensburger® AG. TipToi® and Ravensburger® are registered trademarks or trademarks of Ravensburger® AG, in the Germany and/or other countries. These and all other trademarks referenced in this Software or Documentation are the property of their respective owners. The trademarkes are mentioned for reference only.