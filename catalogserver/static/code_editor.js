var search_box = function(dosearch) {
    var inp = elt('input');
    
};

var language_selector = function() {
    var div = $('<div></div>');
    var languages = [ 'python', 'javascript' ];
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
    var inp = elt('input', {'type': 'text'});
    var select = elt('select');
    var remove = elt('button').text('-');
    tr.append(elt('td', {}, inp), elt('td', {}, select), elt('td', {}, remove));

    inp.change(function() {
        $.get('/api/search/', { q: inp.val() }, function(results) {
            var opt;
            select.empty();
            for (var i in results) {
                opt = $('<option></option>');
                opt.text(results[i].name + " - " + results[i].summary);
                opt.val(results[i].versionptr);
                select.append(opt);
            }
        });
    });

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

    var submit_button = $('<button>Submit</button>');
    submit_button.click(function() {
        var sub = $.extend({}, proto_opts, {
            code: textarea.val(),
            dependencies: deps_table.find('select')
                                    .map(function(_,x) { return $(x).val() })
                                    .toArray()
                                    .sort()
                                    .join(','),
            language: languages.find('option:selected').val(),
        });
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
    
    div.append(textarea, languages, deps_div, $('<br/>'), submit_button);
    return div;
};

// CodeCatalog Snippet http://codecatalog.net/16/119/
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

// CodeCatalog Snippet http://codecatalog.net/49/149/
var label_table = function(dict) {
    var ret = elt('table');
    for (var i in dict) {
        ret.append(elt('tr', {}, 
                       elt('td', {}).text(i),
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
            'Summary': summary_input,
        }),
        code_editor(proto, function(snip) {
            snip.title = title_input.val() || "unnamed";
            snip.summary = summary_input.val();
            submit_callback(snip);
        }));
};
