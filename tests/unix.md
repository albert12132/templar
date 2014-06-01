Introduction to Unix
--------------------

Hello! The first thing you might have noticed about these computers is
that they don't have Windows or MacOS installed. And you're right -
they're running UNIX (Ubuntu to be exact). But fear not! We'll get you
familiar with this new system in no time - by the end of the semester,
this stuff will feel like old hat.

By now, you should already have logged in, registered (make sure you
use your *berkeley.edu* email address) and changed your password by
running `ssh update`.  If you made a typo (e.g. misspelled your name),
don't worry; you can restart the registration program, first by
completing the registration process, and then typing `re-register` at
the prompt and hitting enter.

*Note*: **Please** do not forget your login information - especially
your log-in name (e.g.  cs61a-ba). Memorize your log-in name, e-mail
your log-in name to yourself, etc. If you forget, you'll need to get
another log-in form from your TA and start again. If you forget your
password, you can either e-mail INST at inst@eecs.berkeley.edu, or go
to 333 Soda.

### Logging in from Home

If you don't have access to a school computer for this lab, you can
still try it out: refer to <a href='../lab01/lab01.php'>lab 1</a> for
more details about setting up your home computer.

Meet the Terminal
-----------------

The first thing we're going to do is open the Terminal. To do this,
click on the launcher in the top left corner. Start typing in
"Terminal" and it should autocomplete.  You should see something like
this:

![Opening the Terminal](assets/pick_terminal.png "Figure 1: Opening the
Terminal")

Press "Enter" or click on the Terminal icon and finally, you'll see a
window that looks something like this:


![Terminal](assets/terminal.png "Figure 2: The terminal windw")

This window is called the terminal - this is where you'll be talking
to the computer. You talk to the computer by entering in commands.
Here's a neat command - need to look up a date for this month? Try the
`cal` command by typing `cal` into the terminal, then hitting enter:

![Calendar output](assets/cal_cmd.png "Figure 3: Your first command")

Neat, right? Turns out, these computers can do more than displaying
the current calendar - crazy, right? 

Directories
-----------

The most important thing to learn first is how to use the filesystem.
Unlike in Windows/MacOS, there aren't folders you can
click/drag/double-click. There's not even a 'My Computer' icon in
sight!

That's okay - we're going to learn how to do everything via the
command line (the command line is the terminal). Everything you did on
a visual-based filesystem (i.e. like those found on a Windows/MacOS
system), you can also do via the terminal.

### Directories

First, I'll introduce you to our good friend, `ls`.

`ls` is a command that lists all the files in the current directory.
Oh yes, and what's a directory?  A directory is just like a folder,
e.g. the "My Documents" folder.  When you log in, you are
automatically started off in the home directory, so if we run the `ls`
command right now, it'll display all the files in our home directory:

Try the `ls` command now! 

    star [121] ~ # ls
    star [122] ~ #

Hm - nothing really happened. That's because there's nothing in our
home directory - we just made our account after all! Let's make some
stuff! 

### Making Directories

This leads to another good command: the `mkdir` command.

`mkdir` is a command that makes a new directory (hey now, the command
names make sense!). Unlike `cal` and `ls`, we don't just type `mkdir`
and press enter - we need to specify the name of the folder we want to
create! Since we're well-organized people, let's create a new
directory for this lab, and call it lab0:

    star [122] ~ # mkdir lab0
    star [123] ~ #

When we supply extra 'stuff' to a command (like a folder name, for
instance), we say that we're calling the mkdir command with
parameter(s). Not all commands take arguments (recall `cal`). Some
commands even have optional parameters (`ls`, for instance, has a
bunch of different optional parameters).

Okay, now that we've made our directory, let's make sure it's actually
there - use the `ls` command to make sure that the lab0 directory
exists.

    star [123] ~ # ls
    lab0
    star [124] ~ #

Hey, there's our new directory! Awesome.

### Changing Directories

 To get 'inside' the directory, we have a handy command called `cd`.

`cd` (short for change-directory) is a command that, when given a
directory name as a parameter, takes you into that directory. Enter
the lab0 directory by typing: `cd lab0`

    star [124] ~ # cd lab0
    star [125] ~/lab0 #

Note that the `~` turned into a `~/lab0`. This tells you that you're
currently in the lab0 directory - the `~` stands for the home
directory.

So we're inside the lab0 directory, but there's not much here.  You
can `ls` to make sure that it's empty.  Let's say we want to go back
to the home directory: there are two ways to go back from here.

One way is to enter in the following: `cd .. `

    star [125] ~/lab0 # cd ..
    star [126] ~ #

The `..` is shorthand in UNIX for "the parent directory". The home
directory is the parent directory of the lab0 directory (since the
lab0 directory lives in the home directory).

Alternately, you can type in just: `cd`

    star [125] ~/lab0 # cd
    star [126] ~ #

Running the `cd` command with no parameters is equivalent to returning
to the home directory. This is handy when you're many directories
deep, and you don't want to keep repeating `cd ..` to get back home.

### Removing Directories

We've created them - now, we can destroy them! Er, remove them,
rather. Often, you'll find yourself wanting to delete directories
(say, to organize things). To delete a directory, we use `rm -r`
command, short for remove recursively.  This tells Unix to recursively
go through a folder, deleting the folder and all of its contents
(including empty folders).

Like `mkdir`, `rm -r` takes a directory name as a parameter. Try the
following steps:

1. Create a directory called `my_folder`
2. Run `ls` to see that it's really there
3. Remove the directory using `rm -r my_folder`
4. Run `ls` again to see that it's not there anymore.

Summary: We've learned about the following commands:

* `cal`: displays the current month
* `ls`: lists the current directory contents
* `mkdir`: creates a new directory with a specified name
* `cd` moves into/out of directories
* `rm -r`: removes the given directory

Files
-----

We've done a lot of things so far, but only with directories - we
probably want to be able to actually have stuff in our directories.
So, let's make some files, and learn the commands to manipulate them.

Our first step is to create a file. Notice the distinction between
files and directories. In UNIX, we tend to treat files and directories
separately - for instance, it makes sense to `cd` into a directory,
but it doesn't quite make sense to `cd` into a text file!

Let's create a simple file that has the sentence: 'This semester will
be awesome'

The command we'll use is called `echo`.  `echo` is a command that
simply displays anything you type after the word 'echo':

    star [136] ~ # echo hello
    hello
    star [137] ~ # echo Stop repeating me!
    Stop repeating me!
    star [138] ~ # echo No, you stop!
    No, you stop! 

Some terminology - the words that the computer displays after we hit
the enter button is the output of the echo command. It's sort of like
this picture:

![Echo visual](assets/echo_visual.png "Figure 4: Visualization of
input/output of he echo command")

### Making a file

UNIX has a very nice way of creating files using the command `touch`.
Let's say we want to create a file called `my_file`, we can do this by
doing:

    star [139] ~ # touch my_file
    star [140] ~ # ls
    lab0 my_file

That was easy! We created a new file - to get a glimpse into what's
inside, we can use another command, called `cat`. `cat` is a command
that displays the contents of a given file: 

    star [141] ~ # cat my_file
    star [142] ~ #

The reason why we didn't see anything happen is because `touch`
creates an empty file!

To remove files, we use the `rm` command - this time without the `-r`
option.  Use the `rm` command to delete the `my_file` file:

    star [142] ~ # ls
    lab0 my_file
    star [143] ~ # rm my_file
    star [144] ~ # ls
    lab0

*Warning*: Use `rm` with utmost care! Unlike in Windows/MacOS, there
is no friendly 'Recycle Bin' or 'Trash' where you can restore a
deleted file. In UNIX (at least on these systems), when you `rm` a
file, it's gone. Vanished.  Caput. There's no 'undo-ing' a `rm` - so,
think twice (and thrice!) before using the `rm` command! 

With directories, we were able to make and remove them. However, for
files, we can do even more! 

Let's go ahead and make a new file, because we have removed the one we
made in the previous section. 

    star [139] ~ # touch my_file
    star [140] ~ # ls
    lab0 my_file

Let's add some text to our file. Using the `echo` command from before,
we can add text to our file!

    star [141] ~ # echo "This semester will be awesome" > my_file

For those interested, the `>` symbol means redirect what is usually
shown onto the screen into the file that you specified after the `>`
symbol.  In this case, we're adding the text "This semester will be
awesome" to the file, `my_file`. Be careful though, `>` *overrides*
whatever was originally in the file (ours was originally blank). To
add text to an existing file, use `>>`

### Copying a file

Let's say we wanted to make a copy of this file. Well we can use the
`cp` command.  `cp` takes two parameters, the first is the name of the
file you want to make a copy of, and the second is the name of the new
file you want to copy the first file into. For example, if we wanted
to copy `my_file` into a new and different file called `new_file`,
then we could do so as follows: 

    star [272] ~ # cp my_file new_file
    star [273] ~ # ls
    lab0 my_file  new_file

If we were then to look at each file separately using the `cat`
command, we can see that `new_file` is simply a copy of `my_file`.
Exactly what we wanted. 

    star [275] ~ # cat new_file
    This semester will be awesome

Now a lot of times we will want you to copy a file from our cs61a
account into your own. We can use the `cp` command to do so by
specifying the filepath, which will almost always be given to you.
(For example, something like `~cs61a/lib/shakespeare.txt` is the
filepath for the text file from our 61a account which contains a
Shakespearean sonnet).

What we could do is something like this:

    star [276] ~ # cp ~cs61a/lib/shakespeare.txt shakespeare.txt
    star [277] ~ # ls
    lab0 my_file new_file shakespeare.txt

But here's a handy tip: if we put a period '`.`' as the second
argument to `cp`, we get the same effect: 

    star [278] ~ # cp ~cs61a/lib/shakespeare.txt .
    star [279] ~ # ls
    lab0 my_file new_file shakespeare.txt

The '`.`' is a UNIX shorthand for 'current directory'. So, `cp
~cs61a/lib/shakespeare.txt .` means: Create a new copy of
~cs61a/lib/shakespeare.txt, and put it in the current directory. 

Similarly, if we wanted to, we could copy shakespeare.txt to our lab0
directory by doing: 

    star [280] ~ # cp ~cs61a/lib/shakespeare.txt lab0
    star [281] ~ # ls lab0
    shakespeare.txt

### Moving a File

We can also move a file to a different directory by using the `mv`
command.  `mv` takes in two parameters as well: the first is the
filename that we want to move, and the second is the name of the
directory that we want to move that file into.

    star [275] ~ # mv new_file lab0
    star [275] ~ # ls
    lab0 my_file
    star [276] ~ # cd lab0
    star [277] ~/lab0 # ls
    new_file

We just moved `new_file` into the lab0 directory. As you can see, the
lab0 directory is in the home directory, which is where the `new_file`
originally was.  The name of the directory we are moving the file into
needs to be in the current directory, or else the computer will not
know what directory you are referring to, and will instead rename the
file (more on that later).

However, what if we wanted to move the file back into the home
directory; the home directory is not inside of lab0, so there is no
way to reach it right? No! Just like we could change into a parent
directory by calling cd with '`..`' we can also move a file into the
parent directory by calling `mv` with a filename and '`..`' as
follows:

    star [276] ~/lab0 # ls
    new_file
    star [278] ~/lab0 # mv new_file ..
    star [279] ~/lab0 # ls
    star [279] ~/lab0 # cd
    star [278] ~ # ls
    new_file 

We have just moved `new_file` back into our home directory,
which was a parent directory of the lab0 directory.

### Renaming a File

Lastly, we can rename a file. To rename a file, we can actually also
use the `mv` command. In this case, the `mv` command still takes in
two parameters: the first being the name of the file we want to
rename; however, the second is the new name for the file. 

    star [277] ~/lab0 # mv new_file best_name_ever
    star [278] ~/lab0 # ls
    best_name_ever 

We have just successfully renamed `new_file` to be the filename:
`best_name_ever.` 

### The most useful UNIX command: man

We've shown you a lot of commands and it might become a little
hard to remember what everything does. If you ever forget (and can't
be bothered to come back to this page), there is one useful that'll
help: `man` (short for manual). 

Just run `man` with some other Unix command to find out what it does
(e.g. `man cp`).  `man` will bring up a page inside of the terminal.
The NAME field will give a brief description of what the command does,
and the DESCRIPTION will have a host of extra options you can run the
command with. 

You can navigate forward through the man page with the `Enter/ Return`
key and you can quit with `q` key. 

Running programs: Firefox
-------------------------

These machines come pre-installed with a variety of programs.  If you
continue to use the lab machines, two programs that you'll be
frequently using over the semester are Firefox and Emacs. 

Firefox is a free web browser (like Internet Explorer, Safari, Google
Chrome, etc.). **To open it, you can simply click on the icon on the
left hand side of your screen.**

A recap
-------

Whew! We've covered a lot so far, so let's recap what we've done so
far. 

* How to use commands to navigate the filesystem
    * `ls`, `cd`
* How to create/remove directories
    * `mkdir`, `rm -r`
* How to create/remove/display files
    * `echo`, `rm`, `cat`
* How to move/rename/copy files
    * `mv`, `cp`
* How to redirect output from one command to another
    * i.e. `echo This is my file > new_file`
* How to run programs, and access the Internet with firefox
    * `firefox`
* If you ever forget what a command does
    * `man`

This is fantastic -- definitely all of the commands you'll need for the
semester. However, we have yet to really create/edit/save text files.
And no, Microsoft Word is not installed on these machines. But we have
something better! 

> If you plan to use your own computer for most of your work in this
> course, there are many editors to choose from depending on your
> operating system.  Instead of reading this section on Emacs, start
> reading [Lab 1](../lab01/lab01.php) on selecting an editor.

Our Text Editor: Emacs
----------------------

Emacs is a very popular free text editor, with quite a bit of history
behind it (it was created in 1976!). This is the text editor we'll
primarily be using this semester. However, it's definitely not
required -- some other text editors include:

* Notepad++
* Vim
* Nano
* Sublime Text 2
* TextMate

However, we'll only be talking about Emacs here. Now, Emacs may seem
very intimidating and difficult at first, but don't worry, we'll get
you situated in no time. 

To help us keep track of what we're doing, I'm going to explicitly
state the goals for this section: 

1. Using Emacs, create a new text file called `my_epiphany` in the
   home directory, and type the sentence:

        "This is going to be a pretty good semester."

2. Then, using Emacs, re-open `my_epiphany`, and edit it to instead
   say:

        "This semester is going to be a fantastic semester"

So, let's start with opening up Emacs. It's important where you open
Emacs, because the directory in which you open Emacs determines the
directory that Emacs 'starts off' in. For instance, if I open up Emacs
in the home directory, and I saved a file called `my_file.txt`, then
`my_file.txt` will appear in the home directory.  But more on that
later!

Let's try opening Emacs with the following: 

    star [145] ~ # emacs

One unfortunate side-effect of opening up Emacs like this is
that our terminal is now unresponsive to new commands: 

    star [145] ~ # emacs
    ls
    cd
    helloooo
    you're not working anymore :(

The terminal will only be responsive once you exit Emacs. To avoid
this situation, if you add an ampersand '`&`' after `Emacs`, the
terminal will still be responsive: 

    star [145] ~ # emacs &
    star [146] ~ # ls
    lab0
    star [147] ~ # echo "Hooray, you're listening to me"
    Hooray, you're listening to me 

A window something like this should open up:

![Emacs Splash](assets/emacs_splash.png "Figure 5: The Emacs splash
page.")

This is the 'splash page' for Emacs - later, if you're interested, you
can check out the Emacs Tutorial, but let's not do that right now. (It
is a valuable resource for learning to use Emacs, but it might take
more time than you have during lab! :p) 

### Creating a file in Emacs

Now, let's create our new file - to do that, you can do any of the
following 2 options: 

* Option 1: Go to File menu, and click on Visit New File...

  ![Emacs new file 2](assets/emacs_new2.png "Figure 6: One way to create
  a new file in Emacs")

  Once you've done that, a prompt will appear on the bottom area (this
  is called the mini-buffer), asking for the name of the file you wish
  to create. Type in `my_epiphany` as the file name, and hit enter.
  (See Figure 7 to see what the mini-buffer looks like). 

  ![Emacs minibuffer](assets/emacs_minibuffer.png "Figure 7: The
  mini-buffer")
* Option 2: Use the hot-key `C-x C-f`, then type in `my_epiphany` in
  the mini-buffer. If you're not sure what `C-x C-f` means, then check
  out the "Emacs Hotkeys" section. But for now: `C-x C-f` is a
  two-step process:
    1. First, while holding down `Control` (Ctrl), hit the '`x`' key.
    2. Release the '`x`' key.
    3. Then, while continuing to hold down `Control` (Ctrl), hit the
       '`f`' key.

Now, the Emacs window should turn into a blank page - this is
the newly created `my_epiphany` file. Go ahead and type the sentence:
"This is going to be a pretty good semester." 

![Emacs saving](assets/emacs_saving.png "Figure 8: Our new file.")

Now that we've added our sentence, let's save the file (either doing
`File -> Save` or doing the hotkey `C-x C-s`. You'll know it's saved
when the two stars after the file-name go away (see Figure 8 to see
what I mean). 

Now, exit Emacs (by doing `File -> Quit` , or `C-x C-c`).
Congratulations! You've just created your first file in Emacs. We can
confirm that it does in fact exist by `cat`-ing the file: 

    star [149] ~ # ls
    lab_0 my_epiphany
    star [150] ~ # cat my_epiphany
    This is going to be a pretty good semester.

### Editing a file in Emacs

But wait! We want to edit that file - we want to instead say: "This
semester is going to be a fantastic semester!" 

So, let's edit the file to say this instead. One way we could do this
is open up Emacs using `emacs &`, and use the `File -> Open` (hotkey:
`C-x C-f`) to open up the file (typing in `my_epiphany` in the
mini-buffer): 

![Emacs open](assets/emacs_open.png "Figure 9: Opening a file in Emacs")

Or, we can provide the name of the file as a parameter while opening
up Emacs: 

    star [151] ~ # emacs my_epiphany & 

This does two things at once: 
1. Start Emacs
2. Open up the `my_epiphany` file

Now, modify the file to instead say "This semester is going to be a
fantastic semester", save it, and exit Emacs.  `cat` the file to make
sure that it worked. 

    star [152] ~ # cat my_epiphany
    This semester is going to be a fantastic semester

*Helpful Tip*: If the mini-buffer ever has a prompt that you don't
understand (say, you accidentally hit a command), and you're not sure
what to do, click the mini-buffer and do the hotkey `C-g`. This will
cancel the mini-buffer prompt, and also cancel the command that was
expecting the prompt. 

The Python Interpreter
----------------------

In Computer Science parlance, an interpreter is a program that lets
you interactively 'talk' to a programming language. A Python
Interpreter is thus a program that lets you interactively talk to
Python. The best way to see what I mean is to try it out yourself! 

Just like Firefox and Emacs, we can enter the Python interpreter from
the terminal. To do this, simply type `python` at the terminal: 

    star [153] ~ # python
    Python 3.2.3 (default, Apr 10 2013, 06:11:55)
    [GCC 4.6.3] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

Now, you're talking to Python! The "`>>>`" signifies that the
interpreter is waiting for user input. So, when you type something in
and hit enter, Python will try to evaluate it. It's similar in spirit
to the UNIX terminal prompt, but instead of talking to UNIX, you're
talking to Python. Try typing in a few simple arithmetic expressions. 

    >>> 1 + 2
    3
    >>> 7 * 8 - 9
    47
    >>> (1 + 2) * (3 - 4)
    -3

Notice that you're actively talking to Python - hence, why it's an
interactive program. 

We'll play around in Python more a little later in lab, so let's get
back to more Emacs fun - you can exit the Python interpreter by doing
either of the following: 

* Typing `exit()`, and hitting enter
* Or, doing `C-d`

Emacs, Python, and the Terminal
-------------------------------

The Python interpreter is definitely neat, and allows you to try and
test out little bits of code relatively easily and quickly.  But as
our code gets more complex, typing everything into the interpreter
again and again gets tedious. Emacs comes in handy here, as it allows
our code some permanence. 

Emacs does allow us to edit a file and then immediately run it in a
built-in interpreter, but that can get a little messy on our
instructional machines. To save Emacs (and ourselves) some trouble,
let's couple it with the powerful Unix terminal. You'll hopefully be
spending a lot of time in the terminal anyways, so using a text editor
and a terminal simultaneously becomes an obvious combination. 

Let's start by creating a Python source file, so navigate to the lab0
directory, either 

1. from within the terminal, and running a new Emacs instance from
   within the lab0 folder, OR
2. from within Emacs by typing in "lab0/" before you write the
   filename

Now, create a new file called greet.py - the .py file extension is
important, because: 

* It's convention for Python source files to end in a .py
extension
* Emacs needs the .py at the end to activate the
Python mode

Let's write a very simple, sort-of-silly program that greets you by
name. Don't worry if you don't understand the program (we'll learn
what each of these pieces mean in more depth over the next few weeks): 

    print("Hello world!")
    my_name = "Eric"

    def greet():
        print("Greetings ", my_name, ", how are you today?")
        print("  - Python")

Now, your Emacs screen should look something like this: 

![greet.py](assets/greet.png "Figure 10: Our simple greet.py program")

Let's go back to the terminal and run our little program. 

    star [154] ~/lab0 # python3 -i greet.py

You'll know you did it right if "Hello World" pops up and you're
thrown into a Python interpreter: `>>>`

When you run Python with the -i flag, Python acts as if you had typed
every line in greet.py into the interpreter, line by line. That's why
`Hello world!` appears, since the Python interpreter is evaluating
the first line in greet.py: `print("Hello world!")`

greet.py also defines two things: a `my_name` variable (bound to the
value "`Eric`"), and a function `greet` that, when called, greets a
person (signed by Python, nonetheless!). To make sure it works, do the
following in the Python interpreter: 

1. Get the value of `my_name` by typing `my_name`, then hitting enter
2. Call the `greet` function by typing `greet()`, then hitting enter

If you did it right, your terminal should look something like this: 

    star [155] ~/lab0 # python3 -i greet.py
    Hello World!

    >>> my_name
    'Eric'
    >>> greet()
    Greetings Eric, how are you today? 
        -Python 

Great, it works! However, right now it's currently greeting me - we
probably want it to greet you! Go edit the greet.py file, and change
the value of the `my_name` variable to instead be your name. 

For example, if your name is Stephanie, greet.py should look like: 

    print("Hello World!")
    my_name = "Stephanie"

    def greet():
        print("Greetings ", my_name, ", how are you today?")
        print("  - Python")

Save greet.py in Emacs, then go back to the terminal, kill the current
interpreter session with `Ctrl-D`, and run `python3 -i greet.py`.
Then, call the `greet` function again at the Python prompt `>>>` to
make sure the name was changed.

Congrats! You've completed your first typical work-cycle: edit a file,
run it, edit it again, run it again, etc. This will start feeling
natural as the course progresses (and as you get further in your CS
career!). 

Appendix A: Hotkeys in Emacs
----------------------------

If you watch a pro Emacs user work in Emacs, you'll notice that he/she
never uses the mouse to do anything - everything he/she does is via
hotkeys. 

A hotkey is just a combination/sequence of keys that, when performed,
does some action. For instance, you're all probably familiar with the
copy and paste hotkeys: `Ctrl-c`, and `Ctrl-v` respectively. 

Emacs has a wide variety of hotkeys - pretty much any action can be
done with some sort of hotkey. For instance, the hotkey `C-x C-s` will
save the current buffer/file. 

But let's see how to actually perform these hotkeys: 
* `C-x` means: while holding down the `Control` (Ctrl) key, press the
  `x` key.
* `C-s` means: while holding down the `Control` (Ctrl) key, press the
  `s` key.

`C-x C-s` is two actions, one after another: 

1. First, do `C-x`
2. Then, release both keys.
3. Finally, do `C-s`

To learn more about Emacs, go through the Emacs tutorial. You can
access it from the splash screen or by typing `C-h t`. (First, do
`C-h`, then just type `t`.)

### The Meta Key

Some hotkeys involve the Meta key, such as this hotkey that opens up a
Scheme interpreter: `M-s` 

The lab keyboards do not have a dedicated Meta key (and most laptops
don't either).  Instead, on most computers, you can use the `Alt` key.
Hold down the `Alt` key while pressing the next key in the command.

You can use `Esc` as a "sort of" Meta key. The difference is, you
first press the `Esc` key, then you hit the next key: for instance, to
do `M-s`, you don't hold `Esc` while pressing `s` - you can just do:

1. First press the `Esc` key
2. Then press the `s` key 

### Some useful hotkeys

<table class="txt_table">
  <col width="250px" align="justify" />
  <col align="right" />
  <tr>
    <th> Hotkey </th>
    <th> Description of what it does </th>
  </tr>
  <tr>
    <td> `C-x C-s` </td>
    <td> Save your file. </td>
  </tr>
  <tr>
    <td> `C-x C-f` </td>
    <td> Open a file. If the filename you provide in the minibuffer
    doesn't exist, then Emacs will create a new file for you. </td>
  </tr>
  <tr>
    <td> `C-/`</td>
    <td> Undo. </td>
  </tr>
  <tr>
    <td> `C-w` </td>
    <td> Cut the highlighted region of text. </td>
  </tr>
  <tr>
    <td> `C-y` </td>
    <td> Paste text. </td>
  </tr>
  <tr>
    <td> `M-w` </td>
    <td> Copy the highlighted region of text. </td>
  </tr>
  <tr></tr>
  <tr>
    <td> `C-g` </td>
    <td> Cancel a command (useful if you accidentally did a command,
    and the mini-buffer is prompting you for something). </td>
  </tr>
  <tr>
    <td> `C-x C-c` </td>
    <td> Exit Emacs </td>
  </tr>
</table>

Appendix B: Unix Commands Summary (incomplete list)
---------------------------------------------------

<table class="txt_table">
  <col width="250px" align="justify" />
  <col align="right" />
  <tr>
    <th> Command </th>
    <th> Description </th>
  </tr>
  <tr>
    <td> `cal` </td>
    <td> Displays the current month </td>
  </tr>
  <tr>
    <td> `ls` </td>
    <td> Lists the current directory contents </td>
  </tr>
  <tr>
    <td> `mkdir` </td>
    <td> Creates a new directory with a specified name </td>
  </tr>
  <tr>
    <td> `cd` </td>
    <td> Moves into/out of directories </td>
  </tr>
  <tr>
    <td> `rm -r` </td>
    <td> Removes the given directory </td>
  </tr>
  <tr>
    <td> `echo` </td>
    <td> Outputs user input. </td>
  </tr>
  <tr>
    <td> `cat` </td>
    <td> Displays the contents of a specified file. </td>
  </tr>
  <tr>
    <td> `rm` </td>
    <td> Removes the specified file. </td>
  </tr>
  <tr>
    <td> `mv` </td>
    <td> Move a file to a new destination (can also be used to rename) </td>
  </tr>
  <tr>
    <td> `cp` </td>
    <td> Copy a file to a new destination </td>
  </tr>
  <tr>
    <td> man </td>
    <td> Brings up the manual page for a given command </td>
  </tr>
</table>
