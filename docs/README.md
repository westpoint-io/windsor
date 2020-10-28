# Windsor Docs

This folder contains files that renders terminal commands into gifs used in `windsor` documentation.


## Setup

Just run `npm i` to install the dependencies.

## Recording commands

Run `npm run record <record-name>` and the instructions on how to stop will be show in your terminal.

## Play commands

`npm run play <record-name>` will run in your terminal the commands from that record.

## Rendering

To render the commands into a `gif` run the following command

`npm run render <record-name>`.

The `render` command accepts the parameter `-o <output-file-name>` which names the output file. e.g.

`npm run render <record-name> -- -o <output-dir>`
