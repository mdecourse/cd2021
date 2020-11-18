<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2"/>
<globals/>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="leo.20180902120538.1"><vh>@settings</vh>
<v t="leo.20180902120538.2"><vh>@data qt-gui-plugin-style-sheet</vh></v>
<v t="leo.20180902120538.3"><vh>@string initial_split_orientation = horizontal</vh></v>
</v>
<v t="leo.20180902120523.1"><vh>編輯 reveal</vh>
<v t="leo.20180902120523.2"><vh>@path ./../reveal</vh>
<v t="leo.20200818165234.1"><vh>@clean index.html</vh>
<v t="leo.20200818165301.1"><vh>html</vh>
<v t="leo.20200818165438.1"><vh>head</vh></v>
<v t="leo.20200818165413.1"><vh>body</vh>
<v t="leo.20200818170041.1"><vh>reveal div</vh>
<v t="leo.20200818170222.1"><vh>slides div</vh>
<v t="leo.20200818170328.1"><vh>slide 1</vh></v>
<v t="leo.20200818170535.1"><vh>slide 2</vh></v>
<v t="leo.20200818170636.1"><vh>slide3</vh>
<v t="leo.20200818170909.1"><vh>slide 3-1</vh></v>
<v t="leo.20200818170953.1"><vh>slide 3-2</vh></v>
<v t="leo.20200818171010.1"><vh>slide 3-3</vh></v>
</v>
<v t="leo.20200818170725.1"><vh>slide 4</vh></v>
<v t="leo.20200818171138.1"><vh>slide 5 </vh></v>
<v t="leo.20200818171215.1"><vh>slide 6</vh></v>
<v t="leo.20200818171244.1"><vh>slide 7 </vh></v>
<v t="leo.20200818171312.1"><vh>slide 8</vh></v>
<v t="leo.20200818171344.1"><vh>slide 9</vh></v>
<v t="leo.20200818171412.1"><vh>slide 10</vh></v>
<v t="leo.20200818194721.1"><vh>slide 11</vh></v>
<v t="leo.20200818194751.1"><vh>slide 12</vh></v>
<v t="leo.20200818194812.1"><vh>slide 13</vh>
<v t="leo.20200818194908.1"><vh>slide 13-1</vh></v>
<v t="leo.20200818194933.1"><vh>slide 13-2</vh></v>
</v>
<v t="leo.20200818194840.1"><vh>slide 14</vh></v>
<v t="leo.20200818195039.1"><vh>slide 15</vh></v>
<v t="leo.20200818195105.1"><vh>slide 16</vh>
<v t="leo.20200818195213.1"><vh>slide 16-1</vh></v>
<v t="leo.20200818195237.1"><vh>slide 16-2</vh></v>
<v t="leo.20200818195305.1"><vh>slide 16-3</vh></v>
<v t="leo.20200818195323.1"><vh>slide 16-4</vh></v>
<v t="leo.20200818195339.1"><vh>slide 16-5</vh></v>
</v>
<v t="leo.20200818195147.1"><vh>slide 17</vh></v>
<v t="leo.20200818195403.1"><vh>slide 18</vh></v>
<v t="leo.20200818195426.1"><vh>slide 19</vh></v>
<v t="leo.20200818195445.1"><vh>slide 20</vh></v>
<v t="leo.20200818195502.1"><vh>slide 21</vh></v>
<v t="leo.20200818195520.1"><vh>slide 22</vh></v>
<v t="leo.20200818195541.1"><vh>slide 23</vh></v>
<v t="leo.20200818195604.1"><vh>slide 24</vh></v>
<v t="leo.20200818195625.1"><vh>slide 25</vh></v>
<v t="leo.20200818195643.1"><vh>slide 26</vh></v>
<v t="leo.20200818195701.1"><vh>slide 27</vh></v>
<v t="leo.20200818195715.1"><vh>slide 28</vh></v>
<v t="leo.20200818195731.1"><vh>slide 29</vh></v>
<v t="leo.20200818195748.1"><vh>slide 30</vh></v>
<v t="leo.20200818195800.1"><vh>slide 31</vh></v>
</v>
</v>
</v>
</v>
</v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="leo.20180902120523.1"></t>
<t tx="leo.20180902120523.2"></t>
<t tx="leo.20180902120538.1"></t>
<t tx="leo.20180902120538.2">QTreeWidget {
    /* These apply to the selected item, but not to editing items.*/
    background-color: #ffffec; /* Leo's traditional tree color */
    selection-color: black; /* was white */
    selection-background-color: lightgrey;
    /* font-family: SansSerif; */
    /*font-family: DejaVu Sans Mono;*/
    font-family:YaHei Mono;
    /* 標題字型大小設定 */
    font-size: 20px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal, italic,oblique */
 }

/* Headline edit widgets */
QTreeWidget QLineEdit {
    background-color: cornsilk;
    selection-color: white;
    selection-background-color: blue;
    /*font-family: DejaVu Sans Mono;*/    
    font-family:YaHei Mono;
    /* 沒有特別對應字型大小 */
    font-size: 20px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal, italic,oblique */
}

/* The log panes */
QTextEdit {
    background-color: #f2fdff;
    selection-color: red;
    selection-background-color: blue;
    /* font-family: Courier New; */
    font-family:YaHei Mono;
    /* log font 大小 */
    font-size: 20px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal, italic,oblique */
}

/* The body pane */
QTextEdit#richTextEdit {
    background-color: #fdf5f5; /* A kind of pink. */
    selection-color: white;
    selection-background-color: red;
    /*font-family: DejaVu Sans Mono;*/
    /* font-family: Courier New; */
    font-family:YaHei Mono;
    /* 內文字型大小 */
    font-size: 20px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

QLabel {
    font-family:YaHei Mono;'CherryPy', 'pytz', 'mako', 'beautifulsoup4', 'pymysql', 'peewee'
    /* 下方的 Minibuffer 標題字型大小 */
    font-size: 20px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

/* Editor labels */
QLineEdit#editorLabel {
    background-color: #ffffec;
    font-family:YaHei Mono;
    /* 沒有直接對應字型大小 */
    font-size: 20px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
    border: 2px;
    margin: 2px;
}</t>
<t tx="leo.20180902120538.3">horizontal: body pane to the left
vertical: body pane on the botton</t>
<t tx="leo.20200818165234.1">@language xml
@tabwidth -4
@others</t>
<t tx="leo.20200818165301.1">&lt;!doctype html&gt;
&lt;html lang="en"&gt;
@others
&lt;/html&gt;</t>
<t tx="leo.20200818165413.1">&lt;body&gt;
@others
    &lt;script src="dist/reveal.js"&gt;&lt;/script&gt;
    &lt;script src="plugin/zoom/zoom.js"&gt;&lt;/script&gt;
    &lt;script src="plugin/notes/notes.js"&gt;&lt;/script&gt;
    &lt;script src="plugin/search/search.js"&gt;&lt;/script&gt;
    &lt;script src="plugin/markdown/markdown.js"&gt;&lt;/script&gt;
    &lt;script src="plugin/highlight/highlight.js"&gt;&lt;/script&gt;
    &lt;script&gt;

        // Also available as an ES module, see:
        // https://revealjs.com/initialization/
        Reveal.initialize({
            controls: true,
            progress: true,
            center: true,
            hash: true,

            // Learn about plugins: https://revealjs.com/plugins/
            plugins: [ RevealZoom, RevealNotes, RevealSearch, RevealMarkdown, RevealHighlight ]
        });

    &lt;/script&gt;
&lt;/body&gt;</t>
<t tx="leo.20200818165438.1">&lt;head&gt;
    &lt;meta charset="utf-8"&gt;

    &lt;title&gt;reveal.js – The HTML Presentation Framework&lt;/title&gt;

    &lt;meta name="description" content="A framework for easily creating beautiful presentations using HTML"&gt;
    &lt;meta name="author" content="Hakim El Hattab"&gt;

    &lt;meta name="apple-mobile-web-app-capable" content="yes"&gt;
    &lt;meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"&gt;

    &lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;

    &lt;link rel="stylesheet" href="dist/reset.css"&gt;
    &lt;link rel="stylesheet" href="dist/reveal.css"&gt;
    &lt;link rel="stylesheet" href="dist/theme/black.css" id="theme"&gt;

    &lt;!-- Theme used for syntax highlighting of code --&gt;
    &lt;link rel="stylesheet" href="plugin/highlight/monokai.css" id="highlight-theme"&gt;
&lt;/head&gt;</t>
<t tx="leo.20200818170041.1">&lt;div class="reveal"&gt;
    @others
&lt;/div&gt;</t>
<t tx="leo.20200818170222.1">&lt;!-- Any section element inside of this container is displayed as a slide --&gt;
&lt;div class="slides"&gt;
    @others
&lt;/div&gt;</t>
<t tx="leo.20200818170328.1">&lt;section&gt;
    &lt;a href="https://revealjs.com"&gt;
        &lt;img src="https://static.slid.es/reveal/logo-v1/reveal-white-text.svg" alt="reveal.js logo" style="height: 180px; margin: 0 auto 4rem auto; background: transparent;" class="demo-logo"&gt;
    &lt;/a&gt;
    &lt;h3&gt;The HTML Presentation Framework&lt;/h3&gt;
    &lt;p&gt;
        &lt;small&gt;Created by &lt;a href="http://hakim.se"&gt;Hakim El Hattab&lt;/a&gt; and &lt;a href="https://github.com/hakimel/reveal.js/graphs/contributors"&gt;contributors&lt;/a&gt;&lt;/small&gt;
    &lt;/p&gt;
&lt;/section&gt;

</t>
<t tx="leo.20200818170535.1">&lt;section&gt;
    &lt;h2&gt;Hello There&lt;/h2&gt;
    &lt;p&gt;
        reveal.js enables you to create beautiful interactive slide decks using HTML. This presentation will show you examples of what it can do.
    &lt;/p&gt;
&lt;/section&gt;

</t>
<t tx="leo.20200818170636.1">&lt;!-- Example of nested vertical slides --&gt;
&lt;section&gt;
    @others
&lt;/section&gt;

</t>
<t tx="leo.20200818170725.1">&lt;section&gt;
    &lt;h2&gt;Slides&lt;/h2&gt;
    &lt;p&gt;
        Not a coder? Not a problem. There's a fully-featured visual editor for authoring these, try it out at &lt;a href="https://slides.com" target="_blank"&gt;https://slides.com&lt;/a&gt;.
    &lt;/p&gt;
&lt;/section&gt;

</t>
<t tx="leo.20200818170909.1">&lt;section&gt;
    &lt;h2&gt;Vertical Slides&lt;/h2&gt;
    &lt;p&gt;Slides can be nested inside of each other.&lt;/p&gt;
    &lt;p&gt;Use the &lt;em&gt;Space&lt;/em&gt; key to navigate through all slides.&lt;/p&gt;
    &lt;br&gt;
    &lt;a href="#" class="navigate-down"&gt;
        &lt;img class="r-frame" style="background: rgba(255,255,255,0.1);" width="178" height="238" data-src="https://static.slid.es/reveal/arrow.png" alt="Down arrow"&gt;
    &lt;/a&gt;
&lt;/section&gt;
</t>
<t tx="leo.20200818170953.1">&lt;section&gt;
    &lt;h2&gt;Basement Level 1&lt;/h2&gt;
    &lt;p&gt;Nested slides are useful for adding additional detail underneath a high level horizontal slide.&lt;/p&gt;
&lt;/section&gt;
</t>
<t tx="leo.20200818171010.1">&lt;section&gt;
    &lt;h2&gt;Basement Level 2&lt;/h2&gt;
    &lt;p&gt;That's it, time to go back up.&lt;/p&gt;
    &lt;br&gt;
    &lt;a href="#/2"&gt;
        &lt;img class="r-frame" style="background: rgba(255,255,255,0.1); transform: rotate(180deg);" width="178" height="238" data-src="https://static.slid.es/reveal/arrow.png" alt="Up arrow"&gt;
    &lt;/a&gt;
&lt;/section&gt;</t>
<t tx="leo.20200818171138.1">&lt;section data-auto-animate&gt;
    &lt;h2 data-id="code-title"&gt;Pretty Code&lt;/h2&gt;
    &lt;pre data-id="code-animation"&gt;&lt;code class="hljs" data-trim data-line-numbers&gt;
        import React, { useState } from 'react';

        function Example() {
          const [count, setCount] = useState(0);

          return (
            ...
          );
        }
    &lt;/code&gt;&lt;/pre&gt;
    &lt;p&gt;Code syntax highlighting courtesy of &lt;a href="https://highlightjs.org/usage/"&gt;highlight.js&lt;/a&gt;.&lt;/p&gt;
&lt;/section&gt;

</t>
<t tx="leo.20200818171215.1">&lt;section data-auto-animate&gt;
    &lt;h2 data-id="code-title"&gt;With animations&lt;/h2&gt;
    &lt;pre data-id="code-animation"&gt;&lt;code class="hljs" data-trim data-line-numbers="|4,8-11|17|22-24"&gt;
        import React, { useState } from 'react';

        function Example() {
          const [count, setCount] = useState(0);

          return (
            &amp;lt;div&amp;gt;
              &amp;lt;p&amp;gt;You clicked {count} times&amp;lt;/p&amp;gt;
              &amp;lt;button onClick={() =&amp;gt; setCount(count + 1)}&amp;gt;
                Click me
              &amp;lt;/button&amp;gt;
            &amp;lt;/div&amp;gt;
          );
        }

        function SecondExample() {
          const [count, setCount] = useState(0);

          return (
            &amp;lt;div&amp;gt;
              &amp;lt;p&amp;gt;You clicked {count} times&amp;lt;/p&amp;gt;
              &amp;lt;button onClick={() =&amp;gt; setCount(count + 1)}&amp;gt;
                Click me
              &amp;lt;/button&amp;gt;
            &amp;lt;/div&amp;gt;
          );
        }
    &lt;/code&gt;&lt;/pre&gt;
&lt;/section&gt;

</t>
<t tx="leo.20200818171244.1">&lt;section&gt;
    &lt;h2&gt;Point of View&lt;/h2&gt;
    &lt;p&gt;
        Press &lt;strong&gt;ESC&lt;/strong&gt; to enter the slide overview.
    &lt;/p&gt;
    &lt;p&gt;
        Hold down the &lt;strong&gt;alt&lt;/strong&gt; key (&lt;strong&gt;ctrl&lt;/strong&gt; in Linux) and click on any element to zoom towards it using &lt;a href="http://lab.hakim.se/zoom-js"&gt;zoom.js&lt;/a&gt;. Click again to zoom back out.
    &lt;/p&gt;
    &lt;p&gt;
        (NOTE: Use ctrl + click in Linux.)
    &lt;/p&gt;
&lt;/section&gt;

</t>
<t tx="leo.20200818171312.1">&lt;section data-auto-animate data-auto-animate-easing="cubic-bezier(0.770, 0.000, 0.175, 1.000)"&gt;
    &lt;h2&gt;Auto-Animate&lt;/h2&gt;
    &lt;p&gt;Automatically animate matching elements across slides with &lt;a href="https://revealjs.com/auto-animate/"&gt;Auto-Animate&lt;/a&gt;.&lt;/p&gt;
    &lt;div class="r-hstack justify-center"&gt;
        &lt;div data-id="box1" style="background: #999; width: 50px; height: 50px; margin: 10px; border-radius: 5px;"&gt;&lt;/div&gt;
        &lt;div data-id="box2" style="background: #999; width: 50px; height: 50px; margin: 10px; border-radius: 5px;"&gt;&lt;/div&gt;
        &lt;div data-id="box3" style="background: #999; width: 50px; height: 50px; margin: 10px; border-radius: 5px;"&gt;&lt;/div&gt;
    &lt;/div&gt;
&lt;/section&gt;
</t>
<t tx="leo.20200818171344.1">&lt;section data-auto-animate data-auto-animate-easing="cubic-bezier(0.770, 0.000, 0.175, 1.000)"&gt;
    &lt;div class="r-hstack justify-center"&gt;
        &lt;div data-id="box1" data-auto-animate-delay="0" style="background: cyan; width: 150px; height: 100px; margin: 10px;"&gt;&lt;/div&gt;
        &lt;div data-id="box2" data-auto-animate-delay="0.1" style="background: magenta; width: 150px; height: 100px; margin: 10px;"&gt;&lt;/div&gt;
        &lt;div data-id="box3" data-auto-animate-delay="0.2" style="background: yellow; width: 150px; height: 100px; margin: 10px;"&gt;&lt;/div&gt;
    &lt;/div&gt;
    &lt;h2 style="margin-top: 20px;"&gt;Auto-Animate&lt;/h2&gt;
&lt;/section&gt;
</t>
<t tx="leo.20200818171412.1">&lt;section data-auto-animate data-auto-animate-easing="cubic-bezier(0.770, 0.000, 0.175, 1.000)"&gt;
    &lt;div class="r-stack"&gt;
        &lt;div data-id="box1" style="background: cyan; width: 300px; height: 300px; border-radius: 200px;"&gt;&lt;/div&gt;
        &lt;div data-id="box2" style="background: magenta; width: 200px; height: 200px; border-radius: 200px;"&gt;&lt;/div&gt;
        &lt;div data-id="box3" style="background: yellow; width: 100px; height: 100px; border-radius: 200px;"&gt;&lt;/div&gt;
    &lt;/div&gt;
    &lt;h2 style="margin-top: 20px;"&gt;Auto-Animate&lt;/h2&gt;
&lt;/section&gt;

</t>
<t tx="leo.20200818194721.1">&lt;section&gt;
    &lt;h2&gt;Touch Optimized&lt;/h2&gt;
    &lt;p&gt;
        Presentations look great on touch devices, like mobile phones and tablets. Simply swipe through your slides.
    &lt;/p&gt;
&lt;/section&gt;

</t>
<t tx="leo.20200818194751.1">&lt;section data-markdown&gt;
    &lt;script type="text/template"&gt;
        ## Markdown support

        Write content using inline or external Markdown.
        Instructions and more info available in the [readme](https://revealjs.com/markdown/).

        ```[]
        &lt;section data-markdown&gt;
          ## Markdown support

          Write content using inline or external Markdown.
          Instructions and more info available in the [readme](https://revealjs.com/markdown/).
        &lt;/section&gt;
        ```
    &lt;/script&gt;
&lt;/section&gt;

</t>
<t tx="leo.20200818194812.1">&lt;section&gt;
     @others
&lt;/section&gt;

</t>
<t tx="leo.20200818194840.1">&lt;section id="transitions"&gt;
    &lt;h2&gt;Transition Styles&lt;/h2&gt;
    &lt;p&gt;
        You can select from different transitions, like: &lt;br&gt;
        &lt;a href="?transition=none#/transitions"&gt;None&lt;/a&gt; -
        &lt;a href="?transition=fade#/transitions"&gt;Fade&lt;/a&gt; -
        &lt;a href="?transition=slide#/transitions"&gt;Slide&lt;/a&gt; -
        &lt;a href="?transition=convex#/transitions"&gt;Convex&lt;/a&gt; -
        &lt;a href="?transition=concave#/transitions"&gt;Concave&lt;/a&gt; -
        &lt;a href="?transition=zoom#/transitions"&gt;Zoom&lt;/a&gt;
    &lt;/p&gt;
&lt;/section&gt;

</t>
<t tx="leo.20200818194908.1">&lt;section id="fragments"&gt;
    &lt;h2&gt;Fragments&lt;/h2&gt;
    &lt;p&gt;Hit the next arrow...&lt;/p&gt;
    &lt;p class="fragment"&gt;... to step through ...&lt;/p&gt;
    &lt;p&gt;&lt;span class="fragment"&gt;... a&lt;/span&gt; &lt;span class="fragment"&gt;fragmented&lt;/span&gt; &lt;span class="fragment"&gt;slide.&lt;/span&gt;&lt;/p&gt;

    &lt;aside class="notes"&gt;
        This slide has fragments which are also stepped through in the notes window.
    &lt;/aside&gt;
&lt;/section&gt;
 </t>
<t tx="leo.20200818194933.1">&lt;section&gt;
    &lt;h2&gt;Fragment Styles&lt;/h2&gt;
    &lt;p&gt;There's different types of fragments, like:&lt;/p&gt;
    &lt;p class="fragment grow"&gt;grow&lt;/p&gt;
    &lt;p class="fragment shrink"&gt;shrink&lt;/p&gt;
    &lt;p class="fragment fade-out"&gt;fade-out&lt;/p&gt;
    &lt;p&gt;
        &lt;span style="display: inline-block;" class="fragment fade-right"&gt;fade-right, &lt;/span&gt;
        &lt;span style="display: inline-block;" class="fragment fade-up"&gt;up, &lt;/span&gt;
        &lt;span style="display: inline-block;" class="fragment fade-down"&gt;down, &lt;/span&gt;
        &lt;span style="display: inline-block;" class="fragment fade-left"&gt;left&lt;/span&gt;
    &lt;/p&gt;
    &lt;p class="fragment fade-in-then-out"&gt;fade-in-then-out&lt;/p&gt;
    &lt;p class="fragment fade-in-then-semi-out"&gt;fade-in-then-semi-out&lt;/p&gt;
    &lt;p&gt;Highlight &lt;span class="fragment highlight-red"&gt;red&lt;/span&gt; &lt;span class="fragment highlight-blue"&gt;blue&lt;/span&gt; &lt;span class="fragment highlight-green"&gt;green&lt;/span&gt;&lt;/p&gt;
&lt;/section&gt;</t>
<t tx="leo.20200818195039.1">&lt;section id="themes"&gt;
    &lt;h2&gt;Themes&lt;/h2&gt;
    &lt;p&gt;
        reveal.js comes with a few themes built in: &lt;br&gt;
        &lt;!-- Hacks to swap themes after the page has loaded. Not flexible and only intended for the reveal.js demo deck. --&gt;
        &lt;a href="#" onclick="document.getElementById('theme').setAttribute('href','css/theme/black.css'); return false;"&gt;Black (default)&lt;/a&gt; -
        &lt;a href="#" onclick="document.getElementById('theme').setAttribute('href','css/theme/white.css'); return false;"&gt;White&lt;/a&gt; -
        &lt;a href="#" onclick="document.getElementById('theme').setAttribute('href','css/theme/league.css'); return false;"&gt;League&lt;/a&gt; -
        &lt;a href="#" onclick="document.getElementById('theme').setAttribute('href','css/theme/sky.css'); return false;"&gt;Sky&lt;/a&gt; -
        &lt;a href="#" onclick="document.getElementById('theme').setAttribute('href','css/theme/beige.css'); return false;"&gt;Beige&lt;/a&gt; -
        &lt;a href="#" onclick="document.getElementById('theme').setAttribute('href','css/theme/simple.css'); return false;"&gt;Simple&lt;/a&gt; &lt;br&gt;
        &lt;a href="#" onclick="document.getElementById('theme').setAttribute('href','css/theme/serif.css'); return false;"&gt;Serif&lt;/a&gt; -
        &lt;a href="#" onclick="document.getElementById('theme').setAttribute('href','css/theme/blood.css'); return false;"&gt;Blood&lt;/a&gt; -
        &lt;a href="#" onclick="document.getElementById('theme').setAttribute('href','css/theme/night.css'); return false;"&gt;Night&lt;/a&gt; -
        &lt;a href="#" onclick="document.getElementById('theme').setAttribute('href','css/theme/moon.css'); return false;"&gt;Moon&lt;/a&gt; -
        &lt;a href="#" onclick="document.getElementById('theme').setAttribute('href','css/theme/solarized.css'); return false;"&gt;Solarized&lt;/a&gt;
    &lt;/p&gt;
&lt;/section&gt;
</t>
<t tx="leo.20200818195105.1">&lt;section&gt;
    @others
&lt;/section&gt;

</t>
<t tx="leo.20200818195147.1">&lt;section data-transition="slide" data-background="#4d7e65" data-background-transition="zoom"&gt;
    &lt;h2&gt;Background Transitions&lt;/h2&gt;
    &lt;p&gt;
        Different background transitions are available via the backgroundTransition option. This one's called "zoom".
    &lt;/p&gt;
    &lt;pre&gt;&lt;code class="hljs javascript"&gt;Reveal.configure({ backgroundTransition: 'zoom' })&lt;/code&gt;&lt;/pre&gt;
&lt;/section&gt;

</t>
<t tx="leo.20200818195213.1">&lt;section data-background="#dddddd"&gt;
    &lt;h2&gt;Slide Backgrounds&lt;/h2&gt;
    &lt;p&gt;
        Set &lt;code&gt;data-background="#dddddd"&lt;/code&gt; on a slide to change the background color. All CSS color formats are supported.
    &lt;/p&gt;
    &lt;a href="#" class="navigate-down"&gt;
        &lt;img class="r-frame" style="background: rgba(255,255,255,0.1);" width="178" height="238" data-src="https://static.slid.es/reveal/arrow.png" alt="Down arrow"&gt;
    &lt;/a&gt;
&lt;/section&gt;
</t>
<t tx="leo.20200818195237.1">&lt;section data-background="https://static.slid.es/reveal/image-placeholder.png"&gt;
    &lt;h2&gt;Image Backgrounds&lt;/h2&gt;
    &lt;pre&gt;&lt;code class="hljs html"&gt;&amp;lt;section data-background="image.png"&amp;gt;&lt;/code&gt;&lt;/pre&gt;
&lt;/section&gt;
</t>
<t tx="leo.20200818195305.1">&lt;section data-background="https://static.slid.es/reveal/image-placeholder.png" data-background-repeat="repeat" data-background-size="100px"&gt;
    &lt;h2&gt;Tiled Backgrounds&lt;/h2&gt;
    &lt;pre&gt;&lt;code class="hljs html" style="word-wrap: break-word;"&gt;&amp;lt;section data-background="image.png" data-background-repeat="repeat" data-background-size="100px"&amp;gt;&lt;/code&gt;&lt;/pre&gt;
&lt;/section&gt;
</t>
<t tx="leo.20200818195323.1">&lt;section data-background-video="https://s3.amazonaws.com/static.slid.es/site/homepage/v1/homepage-video-editor.mp4" data-background-color="#000000"&gt;
    &lt;div style="background-color: rgba(0, 0, 0, 0.9); color: #fff; padding: 20px;"&gt;
        &lt;h2&gt;Video Backgrounds&lt;/h2&gt;
        &lt;pre&gt;&lt;code class="hljs html" style="word-wrap: break-word;"&gt;&amp;lt;section data-background-video="video.mp4,video.webm"&amp;gt;&lt;/code&gt;&lt;/pre&gt;
    &lt;/div&gt;
&lt;/section&gt;
</t>
<t tx="leo.20200818195339.1">&lt;section data-background="http://i.giphy.com/90F8aUepslB84.gif"&gt;
    &lt;h2&gt;... and GIFs!&lt;/h2&gt;
&lt;/section&gt;</t>
<t tx="leo.20200818195403.1">&lt;section data-transition="slide" data-background="#b5533c" data-background-transition="zoom"&gt;
    &lt;h2&gt;Background Transitions&lt;/h2&gt;
    &lt;p&gt;
        You can override background transitions per-slide.
    &lt;/p&gt;
    &lt;pre&gt;&lt;code class="hljs html" style="word-wrap: break-word;"&gt;&amp;lt;section data-background-transition="zoom"&amp;gt;&lt;/code&gt;&lt;/pre&gt;
&lt;/section&gt;

</t>
<t tx="leo.20200818195426.1">&lt;section data-background-iframe="https://hakim.se" data-background-interactive&gt;
    &lt;div style="position: absolute; width: 40%; right: 0; box-shadow: 0 1px 4px rgba(0,0,0,0.5), 0 5px 25px rgba(0,0,0,0.2); background-color: rgba(0, 0, 0, 0.9); color: #fff; padding: 20px; font-size: 20px; text-align: left;"&gt;
        &lt;h2&gt;Iframe Backgrounds&lt;/h2&gt;
        &lt;p&gt;Since reveal.js runs on the web, you can easily embed other web content. Try interacting with the page in the background.&lt;/p&gt;
    &lt;/div&gt;
&lt;/section&gt;

</t>
<t tx="leo.20200818195445.1">&lt;section&gt;
    &lt;h2&gt;Marvelous List&lt;/h2&gt;
    &lt;ul&gt;
        &lt;li&gt;No order here&lt;/li&gt;
        &lt;li&gt;Or here&lt;/li&gt;
        &lt;li&gt;Or here&lt;/li&gt;
        &lt;li&gt;Or here&lt;/li&gt;
    &lt;/ul&gt;
&lt;/section&gt;

</t>
<t tx="leo.20200818195502.1">&lt;section&gt;
    &lt;h2&gt;Fantastic Ordered List&lt;/h2&gt;
    &lt;ol&gt;
        &lt;li&gt;One is smaller than...&lt;/li&gt;
        &lt;li&gt;Two is smaller than...&lt;/li&gt;
        &lt;li&gt;Three!&lt;/li&gt;
    &lt;/ol&gt;
&lt;/section&gt;

</t>
<t tx="leo.20200818195520.1">&lt;section&gt;
    &lt;h2&gt;Tabular Tables&lt;/h2&gt;
    &lt;table&gt;
        &lt;thead&gt;
            &lt;tr&gt;
                &lt;th&gt;Item&lt;/th&gt;
                &lt;th&gt;Value&lt;/th&gt;
                &lt;th&gt;Quantity&lt;/th&gt;
            &lt;/tr&gt;
        &lt;/thead&gt;
        &lt;tbody&gt;
            &lt;tr&gt;
                &lt;td&gt;Apples&lt;/td&gt;
                &lt;td&gt;$1&lt;/td&gt;
                &lt;td&gt;7&lt;/td&gt;
            &lt;/tr&gt;
            &lt;tr&gt;
                &lt;td&gt;Lemonade&lt;/td&gt;
                &lt;td&gt;$2&lt;/td&gt;
                &lt;td&gt;18&lt;/td&gt;
            &lt;/tr&gt;
            &lt;tr&gt;
                &lt;td&gt;Bread&lt;/td&gt;
                &lt;td&gt;$3&lt;/td&gt;
                &lt;td&gt;2&lt;/td&gt;
            &lt;/tr&gt;
        &lt;/tbody&gt;
    &lt;/table&gt;
&lt;/section&gt;
</t>
<t tx="leo.20200818195541.1">&lt;section&gt;
    &lt;h2&gt;Clever Quotes&lt;/h2&gt;
    &lt;p&gt;
        These guys come in two forms, inline: &lt;q cite="http://searchservervirtualization.techtarget.com/definition/Our-Favorite-Technology-Quotations"&gt;The nice thing about standards is that there are so many to choose from&lt;/q&gt; and block:
    &lt;/p&gt;
    &lt;blockquote cite="http://searchservervirtualization.techtarget.com/definition/Our-Favorite-Technology-Quotations"&gt;
        &amp;ldquo;For years there has been a theory that millions of monkeys typing at random on millions of typewriters would
        reproduce the entire works of Shakespeare. The Internet has proven this theory to be untrue.&amp;rdquo;
    &lt;/blockquote&gt;
&lt;/section&gt;
</t>
<t tx="leo.20200818195604.1">&lt;section&gt;
    &lt;h2&gt;Intergalactic Interconnections&lt;/h2&gt;
    &lt;p&gt;
        You can link between slides internally,
        &lt;a href="#/2/3"&gt;like this&lt;/a&gt;.
    &lt;/p&gt;
&lt;/section&gt;

</t>
<t tx="leo.20200818195625.1">&lt;section&gt;
    &lt;h2&gt;Speaker View&lt;/h2&gt;
    &lt;p&gt;There's a &lt;a href="https://revealjs.com/speaker-view/"&gt;speaker view&lt;/a&gt;. It includes a timer, preview of the upcoming slide as well as your speaker notes.&lt;/p&gt;
    &lt;p&gt;Press the &lt;em&gt;S&lt;/em&gt; key to try it out.&lt;/p&gt;

    &lt;aside class="notes"&gt;
        Oh hey, these are some notes. They'll be hidden in your presentation, but you can see them if you open the speaker notes window (hit 's' on your keyboard).
    &lt;/aside&gt;
&lt;/section&gt;
</t>
<t tx="leo.20200818195643.1">&lt;section&gt;
    &lt;h2&gt;Export to PDF&lt;/h2&gt;
    &lt;p&gt;Presentations can be &lt;a href="https://revealjs.com/pdf-export/"&gt;exported to PDF&lt;/a&gt;, here's an example:&lt;/p&gt;
    &lt;iframe data-src="https://www.slideshare.net/slideshow/embed_code/42840540" width="445" height="355" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:3px solid #666; margin-bottom:5px; max-width: 100%;" allowfullscreen&gt; &lt;/iframe&gt;
&lt;/section&gt;

</t>
<t tx="leo.20200818195701.1">&lt;section&gt;
    &lt;h2&gt;Global State&lt;/h2&gt;
    &lt;p&gt;
        Set &lt;code&gt;data-state="something"&lt;/code&gt; on a slide and &lt;code&gt;"something"&lt;/code&gt;
        will be added as a class to the document element when the slide is open. This lets you
        apply broader style changes, like switching the page background.
    &lt;/p&gt;
&lt;/section&gt;

</t>
<t tx="leo.20200818195715.1">&lt;section data-state="customevent"&gt;
    &lt;h2&gt;State Events&lt;/h2&gt;
    &lt;p&gt;
        Additionally custom events can be triggered on a per slide basis by binding to the &lt;code&gt;data-state&lt;/code&gt; name.
    &lt;/p&gt;
    &lt;pre&gt;&lt;code class="javascript" data-trim contenteditable style="font-size: 18px;"&gt;
Reveal.on( 'customevent', function() {
console.log( '"customevent" has fired' );
} );
    &lt;/code&gt;&lt;/pre&gt;
&lt;/section&gt;

</t>
<t tx="leo.20200818195731.1">&lt;section&gt;
    &lt;h2&gt;Take a Moment&lt;/h2&gt;
    &lt;p&gt;
        Press B or . on your keyboard to pause the presentation. This is helpful when you're on stage and want to take distracting slides off the screen.
    &lt;/p&gt;
&lt;/section&gt;

</t>
<t tx="leo.20200818195748.1">&lt;section&gt;
    &lt;h2&gt;Much more&lt;/h2&gt;
    &lt;ul&gt;
        &lt;li&gt;Right-to-left support&lt;/li&gt;
        &lt;li&gt;&lt;a href="https://revealjs.com/api/"&gt;Extensive JavaScript API&lt;/a&gt;&lt;/li&gt;
        &lt;li&gt;&lt;a href="https://revealjs.com/auto-slide/"&gt;Auto-progression&lt;/a&gt;&lt;/li&gt;
        &lt;li&gt;&lt;a href="https://revealjs.com/backgrounds/#parallax-background"&gt;Parallax backgrounds&lt;/a&gt;&lt;/li&gt;
        &lt;li&gt;&lt;a href="https://revealjs.com/keyboard/"&gt;Custom keyboard bindings&lt;/a&gt;&lt;/li&gt;
    &lt;/ul&gt;
&lt;/section&gt;

</t>
<t tx="leo.20200818195800.1">&lt;section style="text-align: left;"&gt;
    &lt;h1&gt;THE END&lt;/h1&gt;
    &lt;p&gt;
        - &lt;a href="https://slides.com"&gt;Try the online editor&lt;/a&gt; &lt;br&gt;
        - &lt;a href="https://github.com/hakimel/reveal.js"&gt;Source code &amp;amp; documentation&lt;/a&gt;
    &lt;/p&gt;
&lt;/section&gt;</t>
</tnodes>
</leo_file>
