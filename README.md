# Koala

Koala is a small build tool for Vala programs. It is written in Python and is 
intended to help you build projects written in Vala without using Makefiles
or build-systems like Automake or CMake. Koala's goal is to build your 
projects based on project information specified in the JSON format. 

## How do you install Koala?

Download the sources and place a link on the main.py file under the name 'koala'
in one of the directories listed in your $PATH variable. Furthermore make sure
that the main.py file is executable (chmod +x it otherwise).

## How do you use Koala?

First you create a 'build.json' file in your projects root directory, which may
contain the fields:

+ `name`
	The name of your project
+ `src-dir`
	The path to the directory containing the source files
+ `bin-dir`
	The path to the directory where the output should be written
+ `packages`
	A list of your included packages
+ `arguments`
	A list of additional arguments passed to valac

The following example shows the content of a simple  'build.json' file:

```json
{
  "name" : "my-project",
  "src-dir" : "./src/",
  "bin-dir" : "./bin/",
  "packages"  : ["gtk+-3.0", "glib-2.0"],
  "arguments" : ["-C"]
}
```

Once you created a 'build.json' file, you call Koala and it builds your project
based on your project definitions. If no 'build.json' file is given, it tries
to build your program based on default values. This works as long as you have
no additional package requirements.

### Tags
	build-tool, builder, build-system, vala programing language
