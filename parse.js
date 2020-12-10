#!/usr/bin/env node
// Usage: node parse.js
// Script that creates index.html out of web/template.html and README.md.
// It is written in JS because this code used to be executed on the client side.
// To install dependencies run:
// $ npm install -g jsdom jquery showdown highlightjs
// If running on Mac and modules can't be found after installation add:
// export NODE_PATH=/usr/local/lib/node_modules
// to the ~/.bash_profile or ~/.bashrc file and run '$ bash'.


const fs = require('fs');
const jsdom = require('jsdom');
const showdown  = require('showdown');
const hljs = require('highlightjs');


function main() {
  const html = getMd();
  initDom(html);
  modifyPage();
  const template = readFile('web/template.html');
  const tokens = template.split('<div id=main_container></div>');
  const text = `${tokens[0]} ${document.body.innerHTML} ${tokens[1]}`;
  writeToFile('index.html', text);
}

function getMd() {
  var readme = readFile('README.md');
  const converter = new showdown.Converter();
  return converter.makeHtml(readme);
}

function initDom(html) {
  const { JSDOM } = jsdom;
  const dom = new JSDOM(html);
  const $ = (require('jquery'))(dom.window);
  global.$ = $;
  global.document = dom.window.document;
}

function modifyPage() {
  insertLinks();
  // unindentBanner();
  highlightCode();
}

function insertLinks() {
  $('h2').each(function() {
    const aId = $(this).attr('id');
    const text = $(this).text();
    const line = `<a href="#${aId}" name="${aId}">#</a>${text}`;
    $(this).html(line);
  });
}

function unindentBanner() {
  const montyImg = $('img').first();
  montyImg.parent().addClass('banner');
  const downloadPraragrapth = $('p').first();
  downloadPraragrapth.addClass('banner');
}

function highlightCode() {
  // $('code').not('.python').not('.text').not('.bash').not('.apache').addClass('python');
  $('code').each(function(index) {
      hljs.highlightBlock(this);
  });
  preventPageBreaks();
  // insertPageBreaks();
}

function preventPageBreaks() {
  $(':header').each(function(index) {
    var el = $(this)
    var untilPre = el.nextUntil('pre')
    var untilH2 = el.nextUntil('h2')
    if ((untilPre.length < untilH2.length) || el.prop('tagName') === 'H1') {
      untilPre.add(el).next().add(el).wrapAll("<div></div>");
    } else {
      untilH2.add(el).wrapAll("<div></div>");
    }
  });
}

function insertPageBreaks() {
  insertPageBreakBefore('#print')
}

function insertPageBreakBefore(an_id) {
  $('<div class="pagebreak"></div>').insertBefore($(an_id).parent())
}

function readFile(filename) {
  try {  
    return fs.readFileSync(filename, 'utf8');
  } catch(e) {
    console.error('Error:', e.stack);
  }
}

function writeToFile(filename, text) {
  try {  
    return fs.writeFileSync(filename, text, 'utf8');
  } catch(e) {
    console.error('Error:', e.stack);
  }
}

main();
