var linecount = function(text) {
    return text.split(/\n/).length;
};

var select_on_click = function(elt, modify) {
    elt.focus(function() {
        var text = elt.val();
        elt.oldtext = text;
        elt.oldrows = elt.attr('rows');
        var newtext = modify(text);
        elt.attr('rows', linecount(newtext));
        elt.val(newtext);
        elt.select();
    });
    elt.focusout(function() {
        if (elt.oldtext) {
            elt.attr('rows', elt.oldrows);
            elt.val(elt.oldtext);
        }
    });
    // keep chrome from immediately deselecting
    elt.mouseup(function() { return false });
};
