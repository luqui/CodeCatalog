// CodeCatalog Snippet http://www.codecatalog.net/175/460/
var rate_limited_callback = function(rate, cb) {
    var timeout = null;

    return function() {
        if (timeout) { clearTimeout(timeout); timeout = null; }
        timeout = setTimeout(cb, rate);
    };
};
// End CodeCatalog Snippet

// CodeCatalog Snippet http://www.codecatalog.net/177/469/
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

// CodeCatalog Snippet http://www.codecatalog.net/30/686/
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

// CodeCatalog Snippet http://www.codecatalog.net/183/491/
var keys = function(obj) {
    var r = [];
    for (var key in obj) {
        r.push(key);
    }
    return r;
};
// End CodeCatalog Snippet

// CodeCatalog Snippet http://codecatalog.net/39/669/
var horizontal = function() {
    var row = elt('tr');
    for (var i = 0; i < arguments.length; ++i) {
        var cell = elt('td', {}, arguments[i]);
        row.append(cell);
    }
    return elt('table', {}, row);
};
// End CodeCatalog Snippet

// CodeCatalog Snippet http://codecatalog.net/246/683/
var delegate_method = function(obj, method) {
    if (typeof method == 'string') {
        method = obj[method];
    }
    return function() { return method.apply(obj, arguments) }
};
// End CodeCatalog Snippet

// CodeCatalog Snippet http://www.codecatalog.net/244/684/
var edit_description_field = function()
{
    var edit_comment_input = elt('input', { 'type': 'text', 'class': 'edit_description'});
    var edit_description = horizontal(elt('span').text("Edit summary"), edit_comment_input);
    edit_description.val = delegate_method(edit_comment_input, 'val');
    return edit_description;
};
// End CodeCatalog Snippet

// CodeCatalog Snippet http://www.codecatalog.net/16/119/
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

// CodeCatalog Snippet http://www.codecatalog.net/49/498/
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

//CodeCatalog Snippet http://codecatalog.net/279/782/
var foreach = function(array, body) {
    for (var i = 0; i < array.length; ++i) {
        body(array[i]);
    }
};
// End CodeCatalog Snippet

var embedded_search_tr = function() {
    var tr = elt('tr');
    var choice_to_versionptr = {};
    var current_choice = null;
    var nonsense = elt('div'); // Hack - I don't know what the right way is to do this, but this isn't it.
    nonsense.hide();
    var inp = elt('input');
    inp.autocomplete({ 
    	'source': function(request, response_func) {
    		if (request) {
    			$.get('/api/search/', { q: request.term }, function(results) {
    				var results_formatted = [];
    				foreach(results, function(result) {
    					var choice = result.name + " - " + result.summary;
    					results_formatted.push(choice);
    					choice_to_versionptr[choice] = result.versionptr;
    				});
    				response_func(results_formatted);
    			});
    		}
    	},
    	'select': function(event, ui) {
    		var choice = ui.item.value;
    		if (choice in choice_to_versionptr) {
    			current_choice = choice_to_versionptr[choice];
    			nonsense.text(current_choice); // Hack
    		}
    	}
    });
    
    var remove = elt('button').text('-');
    tr.append(elt('td', {}, inp, nonsense), elt('td', {}, remove));
    remove.click(function() { tr.remove() });
    
    return tr;
};

var code_editor = function(proto, submit_callback) {
    var div = $('<div></div>');
    var textarea = $('<textarea rows="15" style="width:100%"></textarea>');
    var languages = language_selector();
    if (proto.language) { languages.val(proto.language); }
    var deps_tbody = elt('tbody');
    var deps_table = 
        elt('table', {}, 
            elt('thead', {}, 
                elt('tr', {},
                    elt('td').text("Search"),
                    elt('td'))),
            deps_tbody);
    var add_dep = function() {
        var dep = embedded_search_tr();
        deps_tbody.append(dep);
        return dep;
    };
    var add_button = elt('button', {}).text('+');
    add_button.click(add_dep);
    
    var deps_div = elt('div', { 'class': 'deps' }, 
                        elt('b').text('Dependencies'),
                        deps_table, add_button);

    var edit_description = edit_description_field();

    var license = $('<p>By clicking the <i>Submit</i> button, you irrevocably agree to release your contribution under the '
                  + 'terms of the <a href="http://creativecommons.org/publicdomain/zero/1.0/">Creative Commons CC0</a> '
                  + 'license.</p>');
                  
    var submit_button = $('<button>Submit</button>');
    submit_button.click(function() {
    	
    	var deps = [];
    	foreach(deps_table.find('div'), function(div) {
    		deps.push(div.innerHTML);
    	});
    	deps.sort().join(',');
    	
        var sub = $.extend({}, proto_opts, {
            code: textarea.val(),
            dependencies: deps,
            language: languages.find('option:selected').val(),
            comment: edit_description.val()});
        submit_callback(sub);
    });

    var proto_opts = {};
    if (proto) {
        proto_opts.spec_versionptr = proto.spec_versionptr;
        proto_opts.versionptr = proto.versionptr;

        var indeps = proto.dependencies;
        for (var i in indeps) {
            add_dep().val(indeps[i]);
        }

        languages.val(proto.language);
        textarea.val(proto.code);
    }
    else {
        add_dep();
    }
    
    div.append(textarea, languages, deps_div, edit_description, license, submit_button);
    return div;
};

var code_editor_with_title = function(proto, submit_callback) {
    var title_input = elt('input', { type:'text' });
    var summary_input = elt('input', { type:'text' });
    title_input.val(proto.title || "");
    summary_input.val(proto.summary || "");
    return elt('div', {},
        label_table({
            'Title': title_input,
            'Summary': summary_input}),
        code_editor(proto, function(snip) {
            snip.title = title_input.val() || "unnamed";
            snip.summary = summary_input.val();
            submit_callback(snip);
        }));
};
