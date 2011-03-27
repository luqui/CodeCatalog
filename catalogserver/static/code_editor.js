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
    var textarea = $('<textarea rows="30" cols="80"></textarea>');
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
