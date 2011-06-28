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

//CodeCatalog Snippet http://www.codecatalog.net/254/7/
var table_row = function() {
    var tr = elt('tr');
    foreach(arguments, function(arg) {
        tr.append(elt('td', {}, arg));
    });
    return tr;
};
// End CodeCatalog Snippet

var spec_to_address = function(spec) {
    return '/' + spec.versionptr + '/'
};

var search_box = function(options) {
    var e_search_input = options.search_input;
    var e_search_results = options.search_results;
    var go_func = options.go_func;
    
    var style_result_title_func = options.style_result_title_func || function(result) {
        return elt('a', {'href': spec_to_address(result), 'class': 'result_name'}).text(result.name);
    };
    var style_result_summary_func = options.style_result_summary_func || function(result) {
        return elt('span', {'class': 'result_summary'}).text(result.summary);
    };
    
    var top_result = null;
    var top_result_tr = null;
    var results_listing = [];
    var searching = false;
    var enter_while_searching = false;
    var next_search_id = 0;
    var last_search_id = 0;
    
    var results_table = null;
    
    var focus_tr = function(tr) {
        tr = $(tr);
        results_table.find('tr').removeClass('focused');
        tr.addClass('focused');
        top_result = tr.data('spec');
        top_result_tr = tr;
    };
    
    var do_search = function() {
        // do a search for the text
        var query = e_search_input.val();
        if (query.length < 3) {
            e_search_results.empty();
            return;
        }
        
        if (!searching) {
            searching = true;
            enter_while_searching = false;
        }
        
        var search_id = next_search_id = next_search_id + 1;
        
        $.get('/api/search/', { q: query }, function(results) {
            
            if (last_search_id > search_id) {
                return;
            }
            last_search_id = search_id;
            
            results_table = elt('table');
            results_listing = [];
            
            top_result = null;
            if (results.length > 0) {              
                e_search_input.trigger('search',[query]);
                
                foreach(results, function(result) {
                    var result_row = table_row(
                        style_result_title_func(result),
                        style_result_summary_func(result)
                    );
                    
                    result_row.data('spec', result);
                    results_table.append(result_row);
                });
                
                results_table.find(':first-child').addClass('firstchild');
                
                results_table.find('tr').each(function(_, tr) {
                    var tr_element = $(tr).data('result_index', results_listing.length);
                    tr_element.mouseover(function() {
                        focus_tr(tr_element);
                    });
                    tr_element.click(function() {
                        focus_tr(tr_element);
                        go_func(top_result);
                    });
                    
                    results_listing.push(tr_element);
                    
                    if (top_result == null) {
                        focus_tr(tr_element); // Sets top_result to result_row, among other things.
                    }
                });
                results_table.mouseout(function() {
                    focus_tr(results_table.find('tr:first-child'));
                });
            }
            else {
                results_table = elt('div', {'class': 'no_results'}).text("no results");
            }
            
            searching = false;
            if (enter_while_searching) {
                go_func(top_result);
            }
            else { 
                e_search_results.empty();
                e_search_results.append(results_table);
            }
        });
    };
    
    var do_search_rate_limited = rate_limited_callback(300, do_search)
    
    var on_search_edit = function(e){
        if (e.keyCode == 38 /* UP */) {
            var index = top_result_tr.data('result_index');
            var prev_index = (index + results_listing.length - 1) % results_listing.length;
            var prev = results_listing[prev_index];
            focus_tr(prev);
        }
        else if (e.keyCode == 40 /* DOWN */) {
            var index = top_result_tr.data('result_index');
            var next_index = (index + 1) % results_listing.length;
            var next = results_listing[next_index];
            focus_tr(next);
        }
        else if (e.keyCode == 13 /* ENTER */) {
            if (!go_func(top_result)) {
                var was_searching = searching;
                searching = true;
                enter_while_searching = true;
                if (!was_searching) {
                    do_search();
                }
            }
        }
        else
        {
            do_search_rate_limited();
        }
    };
    
    e_search_input.keydown(on_search_edit); 
    e_search_input.focus();
    // Call do_search immediately in-case there was a reload of the page with text in the input box.
    do_search();
};

var embedded_search = function() {
    var span = elt('span');
    var choice_to_versionptr = {};
    var current_choice = null;
    
    var search_input = elt('input');
    var search_results = elt('div').addClass('dep_results_area');
    
    var select = function(choice) {
        current_choice = choice.versionptr;
        span.val(current_choice);
        return true;
    };
    
    var style_result_title_func = function(result) {
        return elt('a', {'href': spec_to_address(result), 'class': 'result_name', 'target': '_blank'}).text(result.name);
    };
    
    search_box({
        'search_input': search_input, 
        'search_results': search_results, 
        'go_func': select,
        'style_result_title_func': style_result_title_func
    });
    
    span.append(search_input);
    span.append(search_results);

    span.val = function(versionptr) {
        if (versionptr) {
            current_choice = versionptr;
            search_input.attr('disabled', 'disabled');
            $.get('/api/specs/' + versionptr + '/active/', function(r) {
                search_input.val(r.name + " - " + r.summary);
                search_results.empty();
            });
            return span;
        }
        else {
            return current_choice;
        }
    };
    
    span.focus = function() {
        search_input.focus();
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

//CodeCatalog Snippet http://www.codecatalog.net/401/4/
var download_script = function(url, callback) {
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.type = 'text/javascript';
    
    var called = false;
    script.onreadystatechange = function () {
        if ((this.readyState == 'loaded' || this.readyState == 'completed') && callback && !called) {
            called = true;
            callback();
        }
    };
    $(script).load(callback);
    script.src = url;
    head.appendChild(script);
};
// End CodeCatalog Snippet

//CodeCatalog Snippet http://www.codecatalog.net/403/2/
var download_stylesheet = function(url) {
    $('head').append(elt('link', {rel: 'stylesheet', href: url}));
};
// End CodeCatalog Snippet

{
    var loaded = false;
    var code_editor_with_deps = function(proto, submit_callback, ret) {
        if (!loaded) {
            download_script("/static/codemirror/codemirror.js", function() {
                ret(code_editor(proto, submit_callback));
            });
            download_stylesheet('/static/codemirror/codemirror.css');
            download_stylesheet('/static/codemirror/theme/neat.css');
        }
        else {
            ret(code_editor(proto, submit_callback));
        }
    };
}

var load_code_editor_deps = (function() {
    var loaded = false;
    return function(cb) {
        if (!loaded) {
            loaded = true;
            download_stylesheet('/static/codemirror/codemirror.css');
            download_stylesheet('/static/codemirror/theme/neat.css');
            download_script("/static/codemirror/codemirror.js", function() {
                cb();
            });
        }
        else {
            cb();
        } 
    }
})();

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
