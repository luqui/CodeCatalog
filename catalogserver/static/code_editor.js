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
    div.val = select.val;
    div.append(select);
    return div;
};

var embedded_search = function() {
    var div = $('<div></div>');
    var inp = $('<input type="text" />');
    var select = $('<select></select>');
    div.append(inp, select);

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

    div.val = function(versionptr) { 
        if (versionptr) {
            $.get('/api/specs/' + versionptr + '/active/', function(result) {
                select.empty();
                var opt = $('<option></option>');
                opt.text(result.name + " - " + result.summary);
                opt.val(versionptr);
                select.append(opt);
            });
        }
        else {
            return select.val(); 
        }
    };
    
    return div;
};

var code_editor = function(proto, submit_callback) {
    var div = $('<div></div>');
    var textarea = $('<textarea rows="30" style="width:100%"></textarea>');
    var languages = language_selector();
    var deps_div = $('<div></div>');
    var deps = [];
    var add_dep = function() {
        var dep = embedded_search();
        deps.push(dep);
        deps_div.append(dep);
        return dep;
    };
    var add_button = $('<button>Add Dependency</button>');
    add_button.click(add_dep);

    var submit_button = $('<button>Submit</button>');
    submit_button.click(function() {
        submit_callback($.extend({}, proto_opts, {
            code: textarea.val(),
            dependencies: deps.map(function(x) { return x.val() })
                              .filter(function (x) { return x })
                              .join(','),
            language: languages.find('option:selected').val(),
        }));
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
    
    div.append(textarea, languages, deps_div, add_button, $('<br/>'), submit_button);
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
