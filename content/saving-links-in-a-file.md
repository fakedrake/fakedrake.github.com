title: Saving links in a file with vimperator
date: 2017-03-20 11:01
tags: vimperator
category: vimperator
slug: saving-links-in-a-file-with-vimperator
author: Chris Perivolaropoulos

I am quite lazy with bibliography. I never keep track of papers and
end up searching for them in google scholar over and over again based
on my (not great) memory. For that I wrote this snippet that helps me
at least keep them around:


    hints.addMode('l', "Save paper link.", function (e) {
      var title = e.innerHTML.replace('<b>', '').replace('</b>', '');
      new io.File('~/Documents/papers.org').write(
        '- [[' + e.href + '][' + title + ']]\n',
        '>>');
    }, function () {
      return util.makeXPath(["h3//a"]);
    });

Put this in a file under `~/.vimperator/plugins/` and in a google
scholar page hit `;l` to activate the hint mode. A link to the paper
you select will be saved in `~/Documents/papers.org`.
