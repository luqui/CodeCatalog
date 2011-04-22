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

// CodeCatalog Snippet http://www.codecatalog.net/30/567/
var language_to_line_comment_map = {
    python: '#',
    javascript: '//',
    haskell: '--',
    c: '//',
    csharp: '//',
    java: '//', 
    ruby: '#',
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

var embedded_search_tr = function() {
    var tr = elt('tr');
    var select = elt('select');
    
    var inp = realtime_input(250, function(value) {
        if (value) {
            $.get('/api/search/', { q: value }, function(results) {
                var opt;
                select.empty();
                for (var i in results) {
                    opt = $('<option></option>');
                    opt.text(results[i].name + " - " + results[i].summary);
                    opt.val(results[i].versionptr);
                    select.append(opt);
                }
            });
        }
        else {
            select.empty();
        }
    });
    var remove = elt('button').text('-');

    tr.append(elt('td', {}, inp), elt('td', {}, select), elt('td', {}, remove));

    remove.click(function() { tr.remove() });

    tr.val = function(versionptr) { 
        if (versionptr) {
            $.get('/api/specs/' + versionptr + '/active/', function(result) {
                select.empty();
                var opt = $('<option></option>');
                opt.text(result.name + " - " + result.summary);
                opt.val(versionptr);
                select.append(opt);
            });
            return tr;
        }
        else {
            return select.val(); 
        }
    };
    
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
                    elt('td').text("Select"),
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

    var license = $('<p>By clicking the <i>Submit</i> button, you irrevocably agree to release your contribution under the '
                  + 'terms of the <a href="http://creativecommons.org/publicdomain/zero/1.0/">Creative Commons CC0</a> '
                  + 'license.</p>');
                  
    var submit_button = $('<button>Submit</button>');
    submit_button.click(function() {
        var sub = $.extend({}, proto_opts, {
            code: textarea.val(),
            dependencies: deps_table.find('select')
                                    .map(function(_,x) { return $(x).val() })
                                    .toArray()
                                    .sort()
                                    .join(','),
            language: languages.find('option:selected').val()});
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
    
    div.append(textarea, languages, deps_div, license, submit_button);
    return div;
};

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
