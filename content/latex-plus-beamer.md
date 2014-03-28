title: LaTeX plus Beamer
date: 2010-10-03 10:20
tags: latex, beamer
category: LaTeX
slug: latex-plus-beamer
author: Chris Perivolaropoulos
summary: Presentations for dinosaurs!

# Prelude

I am making a presentation about plone and I decided Impress is good
but not enough and that i should go with a non-wysiwyg solution:
LaTeX + Beamer. This is the first time I had to use Beamer with Latex
and it was quite a pleasant experience.  So before I get started with
some bumps I stumbled upon a quick recap of how to use beamer.

Start the document with

    :::latex
    \documentclass[arial, pdftex]{beamer}

There are a couple of options available and you are welcome to look
them up(I wont go into them here) but these worked for my case(and I
believe fits most cases)

Also you want to include `\usepackage{graphicx}` if you need graphics in
your presentation(most cases).  Then add some info about the
presentation

    :::latex
    \title{Foo Title}
    \subtitle{Bar Subtitle}
    \author{Chris Perivolaropoulos}
    \institution{university of Patras}

Beamer uses this in some cases making your life easier(mostly in the title page).

A quick summary of the slide definition mechanics of beamer: a slide
can be defined in two ways

    :::latex
    \frame{Sole Contents of the slide}

if you want something really quick (or in my case mostly for the draft version) and

    :::latex
    \begin{frame}{optionally the slide title}
    Contents
    \end{frame}

So next thing you decide when(and if) you want to show a slide with
the contents highlighted according to the context.

    :::latex
    \AtBeginSection[]{\begin{frame}\frametitle{Table of Contents}\tableofcontents[currentsection]\end{frame}}

This would be the case if you want a slide with a table of contents at
the beginning of each section (i would recommend heavy use of sections
and subsections, although i am too lazy to do that more than a
minimum)

It is time to begin the document

    :::latex
    \begin{document}

The first slide is made by beamer based on the information you have
already provided.

    :::latex
    \frame{\titlepage}

# Flow control for pros

Within the slides you can use

    :::latex
    \pause

Whenever you want to stop the slide and wait for a pgdn(eg if show
items in a list one by one, put a `\pause` after each item).

Another way I found useful to control the flow is to use.

    :::latex
    \only{The only thing shown in the slide}

Each frame remains active for a number of slides (or rather is
made of a number of pdf pages if you have ever used office). The
contents of the argument of `\only` will be shown only in the
slides/pages defined by . For example

    :::latex
    \begin{frame}{In the beginning there was HTML}
    \begin{center}
    \includegraphics[width=0.5\textwidth]{html.pdf} \\% vector graphics
    \vspace{1cm}
    \only{\vspace{16pt}}
    \only{http://foo.com/about.html}
    \only{http://foo.com/folder/item.html}
    \end{center}
    \end{frame}

A couple other useful things are shown here:

one if you want somewhere to have an empty line and then have
something appear there `\only{\\}` will not work. I know it would be
handy but LaTeX gets confused this way. What you do is put the size
of the fonts +2 for the space between the lines.

Also it is good to use the center environment which&#x2026;centers
everything in the slide. Be aware that this also means that if we
had omitted the `\only{\vspace{16pt}}` line would screw up the
"effect" of the text appearing under the image because the size of
the content in step 2 is bigger than that of step one, so the
centering would "mess" things up. Another way to have the same
effect is to use a `\pause` instead of `\only{\vspace{16pt}}`. I
dont have a preference.

# Vector graphics

Notice now the `\includegraphics` line in the above exaple. I love
vector graphics and I love inkscape. Inkscape can produce pdf
files(save as->\*.pdf) readable by LaTeX in the way you see
above. Keep in mid though that you should convert any text in your
drawing to paths by or it will not be in the pdf(even though
inkscape's dialog claims to be able to do that for you) and also to
be careful if you are saving it as a page or as a drawing. If you
save as a page only the page is rendered when you include the file in
LaTeX, as a drawing is the way to go in most cases.

# For the boring (or how to show statistics properly)

In my talk i also have some bar charts. What most documentation and
forums suggested for that was a package called pgfplots. DONT USE
THAT. It stole more than 4 hours of my life to produce a mediocre
result. Use R instead. In case you are not familiar with it R is a
language focused on dealing with statistics (package is `r-base` for
ubuntu and `r` for arch).

It can produce REALLY easily bar charts that look the way you expect
them to IF you **don't** use sweave. Sweave is a tool that is supposed
to provide a friendly bridge between R and LaTeX. It works the way
you expect it to but (as many latex modules) is poorly documented
and most importantly the workflow of working with it is very
inefficient. (Note that it has the advantage that it can be
automated meaning that if you plan to frequently work with plots and
graphs in LaTeX you should definitely look into it, if not stay away
as I would rather have done from the getgo).

Instead i ended up being very happy and productive using the R shell
and making it export what I wanted in .pdf graphics files. I will not
go into detail of how to use R. It is really well documented and I am
not by far qualified to say anything about R except that it saved me
loads of time.

# You're good to go

This is the wisdom I have acquired so far from writing my
presentation. I hope this saves people some time and energy.