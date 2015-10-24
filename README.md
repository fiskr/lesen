# Lesen

[Lesen](https://en.wiktionary.org/wiki/lesen#German) is a literate programming tool.


## Syntax

The syntax takes after noweb.

`@` is used to start a document block
`<< ... >>=` is used to start a code block, where `...` designates the name of that block to be referenced later.

The default root code block is `<<*>>=` just like with noweb.

`<< ... >>` can be used in a code block to reference another code block

    @ this is a document block
    Anything I write here will be output by `to-documentation.py`

    <<this is a code block>>=
    // 'this is a code block' is the name of this codeblock
    function fib(n){
      if (n === 0)
        return 0
      else if (n === 1)
        return 1
      else
        return sum(fib(sub(n,1)), fib(sub(n,2)))
    }

    <<main.js>>=
      // this references the above code block
      <<this is a code block>>


## Why Another?
There are lots of literate programming tools out there.
Let's survey some basic differences between then, and discuss motivations for creating Lesen.

### CWEB, noweb, etc.

I actually started learning literate programming with [noweb](http://www.cs.tufts.edu/~nr/noweb/).

It's an awesome tool. I read an [introduction](http://www.cs.tufts.edu/~nr/noweb/johnson-lj.pdf) and an [IEEE article](http://www.cs.tufts.edu/~nr/pubs/lpsimp.pdf) published by the author of noweb.

I kept running into problems getting the thing to build though.

I downloaded version [2.11b](ftp://www.eecs.harvard.edu/pub/nr/) and tried installing it on Debian 8, "Jessie".
After quite some frustration, I tried it on my Mac Book Pro, running El Capitan.
No dice. Xcode didn't seem to want to permit `-ansi -pedantic` flags for `gcc`.
Even if I could get that accomplished, who knows how many more problems lie in the way before finally being able to use the tool.

Luckily for me, I found out that Debian has a noweb package that I can install with aptitude. What great luck!

I started using the tool and found that so many "features" got in the way of the initial purpose.
It was very LaTeX focused, which I was happy about; however, configurations and features abstracted from me kept preventing me from properly extracting the code or documentation.

I persevered, but at this point I went in search of a more modern version of noweb that might be more approachable (especially if I want to sell this whole literate programming thing to my coworkers and fellow programmers).


### Modern Tools
Let's look at a few examples:

#### jostylr/literate-programming

I am sure this tool is great, but I was looking for something _easy_ and _flexible_.

> This requires node.js and npm to be installed.

Python may not be universal, but it is likely more widespread than node.js and npm.

Furthermore, I would rather not require installing a package manager to run what should be simple code.

>It uses markdown as the basic document format with the code to be weaved together being delimited by each line having 4 spaces as is typical for markdown. Note that it requires spaces but not tabs.

Though I set out with LaTeX in mind for Lesen, I wanted to offer flexibility such that weaving tool dictated nothing about what document format you are using.
I created LaTeX headers and footers, as well as special ways to format the code. Some similar functionality was included for Markdown, but honestly - you could write TeX straight in there and not use Lesen's special functions.

Lesen was designed with flexibility in mind - for both what kind of code you are writing, and what kind of documentation you are trying to write.

#### jashkenas/docco

Well, [Docco](http://jashkenas.github.io/docco/) seems fairly flexible! It's small (only 100 lines), and though it requires npm, you can find implementations in other languages like in Python, you have [Pycco](http://fitzgen.github.io/pycco/).
In fact, it has been ported to Lua, Go, PHP, .NET, Ruby, and even POSIX shell!

So what's my beef?

Though there is great support for building your own templates, the tools seems focused on HTML documentation.
I want something that doesn't prefer any given document type over another - where the tool is agnostic to the content.

#### zyedidia/Literate

[Literate](http://zbyedidia.webfactional.com/literate/) is pretty cool too: inspired by CWEB, supports TeX but is modern and supports Markdown too.
It's feature rich, but it's also large. Even though it's implemented in Lua (which for me is associated with low-impact, small scripts that you might even be able to run over an embedded system), it's truly setup as a project. The `weave.lit` file is over 600 lines, though I can't tell how much of that is the documentation.

I wanted to get away from having a huge project that requires you to _install_ software to run a script.
No makefiles, no complexity - just simple, easy, and type-agnostic.

### Conclusion

In the end, I was dissatisfied. I wanted something super easy to use. Not just that, but the promises of literate programming meant that our tools should be _more_ accessible, and easier to learn and understand.

Why did every tool I tried seem to quickly jump off the deep end into dependencies, abstractions, and jargon. Why create such high-context words for `weave` to mean "generate documentation" or `tangle` to mean "extract code"?
I wanted something more accessible - something low-context.

Driving home, my mind kept wandering to this problem and I began to fantasize writing my own tool.
Over time those fantasies became more serious - I realized how simple it could be to implement my own tool.

So I sat down, and in a day had `to-documentation.py` completed. The next day I finished `to-code.py`.
They aren't perfect. They aren't even finished completely. (And perhaps it could be said they will never be finished, merely abandoned).

There are probably many bugs left lurking, waiting for me to find.
There are definitely better ways to write the same code, and package it in modules that are simple and powerful.

But in the end, I solved my problem. Now literate programming is easy, and I hope, more accessible.
