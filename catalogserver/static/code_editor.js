// CodeCatalog Snippet http://www.codecatalog.net/175/1/
var rate_limited_callback = function(rate, cb) {
    var timeout = null;

    return function() {
        if (timeout) { clearTimeout(timeout); timeout = null; }
        timeout = setTimeout(cb, rate);
    };
};
// End CodeCatalog Snippet

// CodeCatalog Snippet http://www.codecatalog.net/177/2/
var realtime_input = function(rate, cb) {
    var input = elt('input', {'type':'text'});
    var pvalue = null;
    var rlcb = rate_limited_callback(rate, function() { 
        var value = input.val();
        if (value == pvalue) return;
        pvalue = value;
        cb(value);
    });
    return input.keydown(rlcb).change(rlcb).blur(rlcb);
};
// End CodeCatalog Snippet

//CodeCatalog Snippet http://www.codecatalog.net/30/11/
var language_to_line_comment_map = {
    python: '#',
    javascript: '//',
    haskell: '--',
    c: '//',
    cpp: '//',
    csharp: '//',
    java: '//', 
    ruby: '#',
    php: '//'
};
// End CodeCatalog Snippet

// CodeCatalog Snippet http://www.codecatalog.net/183/1/
var keys = function(obj) {
    var r = [];
    for (var key in obj) {
        r.push(key);
    }
    return r;
};
// End CodeCatalog Snippet

// CodeCatalog Snippet http://www.codecatalog.net/39/6/
var horizontal = function() {
    var row = elt('tr');
    for (var i = 0; i < arguments.length; ++i) {
        var cell = elt('td', {}, arguments[i]);
        row.append(cell);
    }
    return elt('table', {}, row);
};
// End CodeCatalog Snippet

// CodeCatalog Snippet http://www.codecatalog.net/246/2/
var delegate_method = function(obj, method) {
    if (typeof method == 'string') {
        method = obj[method];
    }
    return function() { return method.apply(obj, arguments) }
};
// End CodeCatalog Snippet

// CodeCatalog Snippet http://www.codecatalog.net/244/6/
var edit_description_field = function()
{
    var edit_comment_input = elt('input', { 'type': 'text', 'class': 'edit_description'});
    var edit_description = horizontal(elt('span').text("Comment"), edit_comment_input);
    edit_description.val = delegate_method(edit_comment_input, 'val');
    return edit_description;
};
// End CodeCatalog Snippet

// CodeCatalog Snippet http://www.codecatalog.net/16/3/
var elt = function(name, attrs) {
    var r = $(document.createElement(name));
    if (attrs) {
        for (var i in attrs) {
            r.attr(i, attrs[i]);
        }
    }
    for (var i = 2; i < arguments.length; ++i) {
        r.append(arguments[i]);
    }
    return r;
};
// End CodeCatalog Snippet

// CodeCatalog Snippet http://www.codecatalog.net/49/5/
var label_table = function(dict) {
    var ret = elt('table');
    for (var i in dict) {
        ret.append(elt('tr', {}, 
                       elt('td', {'width': '1', 'class': 'label'}).text(i),
                       elt('td', {}, dict[i])));
    }
    return ret;
};
// End CodeCatalog Snippet

// CodeCatalog Snippet http://www.codecatalog.net/37/2/
var button = function(text, click) {
    var r = elt('button');
    r.text(text);
    r.click(click);
    return r;
};
// End CodeCatalog Snippet

var language_selector = function() {
    var div = $('<div></div>');
    var languages = keys(language_to_line_comment_map);
    var select = $('<select></select>');
    for (var i in languages) {
        var opt = $('<option></option>');
        opt.val(languages[i]);
        opt.text(languages[i]);
        select.append(opt);
    }
    div.val = function(newval) {
        if (newval) {
            select.find('option').attr('selected', undefined);
            select.find('option[value="' + newval + '"]').attr('selected', 'selected');
        }
        else {
            return select.val();
        }
    };
    div.append(select);
    return div;
};

// CodeCatalog Snippet http://www.codecatalog.net/279/1/
var foreach = function(array, body) {
    for (var i = 0; i < array.length; ++i) {
        body(array[i]);
    }
};
// End CodeCatalog Snippet

//CodeCatalog Snippet http://www.codecatalog.net/303/2/
var make_auto_complete = function(options) {
    var generate_options = options['generate_options'];
    var format = options['format'] || function(x) { return x };
    var select = options['select'] || function() { };
    var stylize = options['stylize'] || function(uimenu) { uimenu.width(element.width()); };
	
    var choice_to_val = {};
    var span = elt('span');
    var element = elt('input').autocomplete({
    	'source': function(request, response_func) {
            if (request) {
            	generate_options(request.term, function(results) {
                    var results_formatted = [];
                    foreach(results, function(result) {
                        var choice = format(result);
                        results_formatted.push(choice);
                        choice_to_val[choice] = result;
                    });
                    response_func(results_formatted);
                });
            }
        },
        'select': function(event, ui) {
            var choice = ui.item.value;
            if (choice in choice_to_val) {
                select(choice_to_val[choice]);
            }
        },
        'appendTo': span,
        'open': function() {
        	stylize(span.find('.ui-menu'));
        }});
    return element.add(span);
};
// End CodeCatalog Snippet

var spec_to_search_result = function(spec) {
    var result = spec.name;
    if (spec.summary) {
        result += " - " + spec.summary;
    }
    return result;
};

var catalog_search_with_autocomplete = function(select, stylize) {
    return make_auto_complete({
    	'generate_options': function(term, response) {
    	    if (term.length > 2) {
    	        $.get('/api/search/', { q: term }, response);
    	    }
    	    else {
    	        response([]);
    	    }
        },
        'format': spec_to_search_result,
        'select': select,
        'stylize': stylize});
};

var embedded_search = function() {
    var span = elt('span');
    var choice_to_versionptr = {};
    var current_choice = null;
    
    var select = function(choice) {
        current_choice = choice.versionptr;
    	inp.attr('disabled', 'disabled');
    };
    
    var inp = catalog_search_with_autocomplete(select, null);
    
    span.append(inp);

    span.val = function(versionptr) {
        if (versionptr) {
            current_choice = versionptr;
            inp.attr('disabled', 'disabled');
            $.get('/api/specs/' + versionptr + '/active/', function(r) {
                inp.val(r.name + " - " + r.summary);
            });
            return span;
        }
        else {
            return current_choice;
        }
    };
    
    span.focus = function() {
        inp.focus();
    };
    
    return span;
};

var editable_list = function(widget_factory) {
    var table = elt('table');
    var objects = [];
    var add_button = elt('button').text('+');
    
    var add = function() {
        var thing = widget_factory();
        var remove_button = elt('button').text('-');
        var span = elt('span', {'class': 'thing'}, thing);
        span.data('thing', thing);
        var tr = elt('tr', {}, elt('td', {}, span), elt('td', {}, remove_button));
        remove_button.click(function() {
            tr.remove();
        });
        table.append(tr);
        if ('focus' in thing) { thing.focus(); }
        return thing;
    };
    add_button.click(add);

    var div = elt('div', {}, table, add_button);
    div.val = function(vals) {
        if (vals) {
            table.empty();
            foreach(vals, function(val) { add().val(val) });
            return div;
        }
        else {
            var ret = [];
            table.find('.thing').each(function(ix,elem) { 
                ret.push($(elem).data('thing').val());
            });
            return ret;
        }
    };

    return div;
};

//CodeCatalog Snippet http://www.codecatalog.net/399/1/
var language_to_codemirror_mode = {
    "python": { url: 'http://codemirror.net/mode/python/python.js', mime: 'text/x-python' },
    "javascript": { url: 'http://codemirror.net/mode/javascript/javascript.js', mime: 'text/javascript' },
    "haskell": { url: 'http://codemirror.net/mode/haskell/haskell.js', mime: 'text/x-haskell' },
    "c": { url: 'http://codemirror.net/mode/clike/clike.js', mime: 'text/x-csrc' },
    "cpp": { url: 'http://codemirror.net/mode/clike/clike.js', mime: 'text/x-c++src' }, 
    "csharp": { url: 'http://codecatalog.net/static/codemirror/mode/clike/clike.js', mime: 'text/x-csharp' },
    "java": { url: 'http://codemirror.net/mode/clike/clike.js', mime: 'text/x-java' }
};
// End CodeCatalog Snippet

//CodeCatalog Snippet http://www.codecatalog.net/401/3/
var download_script = function(url, callback) {
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.onreadystatechange = function () {
        if (this.readyState == 'complete') callback();
    };
    script.onload = callback;
    script.src = url;
    head.appendChild(script);
};
// End CodeCatalog Snippet

var code_editor = function(proto, submit_callback) {
    var div = $('<div></div>');
    var textarea = CodeMirror(div[0], { 
        theme: 'neat', 
        indentUnit: 4,
        mode: 'text/plain',
        tabMode: 'indent'});
    
    var load_language = function(language) { 
        if (language in language_to_codemirror_mode) {
            var mode_info = language_to_codemirror_mode[language];
            download_script(mode_info.url, function() {
                textarea.setOption('mode', mode_info.mime);
            });
        }
        else {
            textarea.setOption('mode', 'text/plain');
        }
    };
    
    var languages = language_selector();
    languages.val('javascript');
    load_language(languages.val());
    
    languages.find('select').change(function() {
        load_language(languages.val());
    });
    
    if (proto.language) { languages.val(proto.language); }

    var deps_table = editable_list(embedded_search);

    var deps_div = elt('div', { 'class': 'deps' }, 
                        elt('b').text('Dependencies'),
                        deps_table);

    var edit_description = edit_description_field();

    var license = $('<p>By clicking the <i>Submit</i> button, you irrevocably agree to release your contribution under the '
                  + 'terms of the <a href="http://creativecommons.org/publicdomain/zero/1.0/">Creative Commons CC0</a> '
                  + 'license.</p>');
                  
    var submit_button = button("Submit", function() {
    	var deps = deps_table.val();
        deps.sort();
    	
        var sub = $.extend({}, proto_opts, {
            code: textarea.getValue(),
            dependencies: deps.join(','),
            language: languages.find('option:selected').val(),
            comment: edit_description.val()});
        submit_callback(sub);
    });

    var proto_opts = {};
    if (proto) {
        proto_opts.spec_versionptr = proto.spec_versionptr;
        proto_opts.versionptr = proto.versionptr;

        if (proto.dependencies) deps_table.val(proto.dependencies);
        if (proto.language)     languages.val(proto.language);
        if (proto.code)         textarea.setValue(proto.code);
    }
    
    div.append(languages, deps_div, edit_description, license, submit_button);
    return div;
};

var code_editor_with_title = function(proto, submit_callback) {
    var title_input = elt('input', { type:'text', 'class':'title_input' });
    var summary_input = elt('input', { type:'text', 'class':'summary_input'});
    title_input.val(proto.title || "");
    summary_input.val(proto.summary || "");
    return elt('div', {},
        label_table({
            'Title': title_input,
            'Summary': summary_input}).addClass('title_summary_table'),
        code_editor(proto, function(snip) {
            snip.title = title_input.val() || "unnamed";
            snip.summary = summary_input.val();
            submit_callback(snip);
        }));
};
