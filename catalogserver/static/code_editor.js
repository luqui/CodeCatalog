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

// CodeCatalog Snippet http://www.codecatalog.net/30/9/
var language_to_line_comment_map = {
    python: '#',
    javascript: '//',
    haskell: '--',
    c: '//',
    csharp: '//',
    java: '//', 
    ruby: '#'
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

//CodeCatalog Snippet http://www.codecatalog.net/309/1/
var on_enter = function(element, callback) {
    return element.keypress(function(e){
        if(e.which == 13) {
            callback();
        }
    });
};
// End CodeCatalog Snippet

var spec_to_address = function(spec) {
    return '/' + spec.versionptr + '/'
};

var search_box = function(e_search_input, e_search_results, go_func) {
    var top_result = null;
    var searching = false;
    var enter_while_searching = false;
    var next_search_id = 0;
    var last_search_id = 0;
    
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
            
            var results_table = elt('table');
            top_result = null;
            if (results.length > 0) {
                e_search_input.trigger('search',[query]);
                foreach(results, function(result) {
                    var result_row = table_row(
                            elt('a', {'href': spec_to_address(result), 'class': 'result_name'}).text(result.name), 
                            elt('span', {'class': 'result_summary'}).text(result.summary));
                    if (top_result == null) {
                        top_result = result;
                        result_row.addClass('focused');
                    }
                    result_row.data('spec', result);
                    results_table.append(result_row);
                });
                
                results_table.find(':first-child').addClass('firstchild');
                
                var focus_tr = function(tr) {
                    tr = $(tr);
                    results_table.find('tr').removeClass('focused');
                    tr.addClass('focused');
                    top_result = tr.data('spec');
                };
                
                results_table.find('tr').each(function(_, tr) {
                    $(tr).mouseover(function() {
                        focus_tr(tr);
                    });
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
    
    e_search_input.keyup(rate_limited_callback(300, do_search));
    
    // Call do_search immediately in-case there was a reload of the page with text in the input box.
    do_search();
    
    on_enter(e_search_input, function() {
        if (!go_func(top_result)) {
            var was_searching = searching;
            searching = true; // we will eventually get the keyup for the enter press!
            enter_while_searching = true;
            if (!was_searching) {
                do_search();
            }
        }
    });
    
    e_search_input.focus();
};

var embedded_search = function() {
    var span = elt('span');
    var choice_to_versionptr = {};
    var current_choice = null;
    
    var search_input = elt('input');
    var search_results = elt('div').addClass('results_area');
    
    var select = function(choice) {
        current_choice = choice.versionptr;
        search_input.attr('disabled', 'disabled');
    };
    
    //var inp = catalog_search_with_autocomplete(select, null);
    search_box(search_input, search_results, select);
    
    span.append(search_input);
    span.append(search_results);

    span.val = function(versionptr) {
        if (versionptr) {
            current_choice = versionptr;
            search_input.attr('disabled', 'disabled');
            $.get('/api/specs/' + versionptr + '/active/', function(r) {
                search_input.val(r.name + " - " + r.summary);
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

var code_editor = function(proto, submit_callback) {
    var div = $('<div></div>');
    var textarea = $('<textarea rows="15" style="width:100%"></textarea>');
    var languages = language_selector();
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
            code: textarea.val(),
            dependencies: deps.join(','),
            language: languages.find('option:selected').val(),
            comment: edit_description.val()});
        submit_callback(sub);
    });

    var proto_opts = {};
    if (proto) {
        proto_opts.spec_versionptr = proto.spec_versionptr;
        proto_opts.versionptr = proto.versionptr;

        deps_table.val(proto.dependencies);
        languages.val(proto.language);
        textarea.val(proto.code);
    }
    
    div.append(textarea, languages, deps_div, edit_description, license, submit_button);
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
