# OpenAPI-extension-remover
A tool to remove extensions of an OpenAPI document so that the resulting file conformes to the specification and can be used by other OpenAPI tools.

## Why did I create this tool?
One day I wanted to generate HTML from my OpenAPI document but I couldn't because the tool that I was using doesn't support vendor extensions (which is a part of the OpenAPI documentation). As such, to make the process more expedite I made this simple tool.

## Future work
In the future, if the need arises I plan to evolve this tool to become an OpenAPI command line utility.

## Notes
This project welcomes any improvement by pull request.

# How to install?
Execute `sudo pip3 install removeOasExtension` on a terminal to system-wide install the tool. Exclude the pip version
 if you only have one version of Python installed and don't need to differentiate it.

# Usage
Basic usages:

**Read from stdin and output to stdout**: removeOasExtension < cat sample.json



