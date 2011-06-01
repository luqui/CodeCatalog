// settings: { editurl, csrf_token }
// Adds a little blue "edit" link next to every element with class .editable.
// If it also has class .editarea, the edit box will be a textarea instead of a
// text input.

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

var editable = function(settings) {
    var makeEditWidget = function(proto) {
        if (proto.hasClass('editarea')) {
            return $('<textarea rows="30" cols="72"></textarea>').val(proto.text());
        }
        else {
            return $('<input type="text" size="72" />').val(proto.text());
        }
    };

    var makeEditBox = function(proto) {
        var span = $('<div/>');
        var editbox = makeEditWidget(proto);
        editbox.val(proto.text());
        var button  = $('<input type="button" value="OK" />');
        span.append(editbox).append(button);

        button.click(function() {
            proto.text(editbox.val());
            var newelt = makeLinkTag(proto);
            span.replaceWith(newelt);
            settings.onedit(newelt)
        });
        return span;
    };
    var makeLinkTag = function(proto) {
        var div = elt('div');
        var editable = proto.clone();
        var empty = proto.text().length == 0;
        var button_text = empty ? "add " + proto.attr('name') : "edit";
        var editlink = elt('a', {'href':'#', 'class':'dynamic_link'}).text(button_text);
        if (!empty) {
            editlink.addClass('dynamic_link_after_text');
        }
        else {
            div.addClass('empty_editable');
        }
        div.append(editable).append(editlink);

        editlink.click(function() {
            if (settings.custom_on_click && !settings.custom_on_click()) return;
            div.replaceWith(makeEditBox(editable));
            return false;
        });
        return div;
    };
    var installEditButtons = function() {
      $('.editable').each(function(x,e) { 
        var je = $(e);
        var editable = makeLinkTag(je);
        je.replaceWith(editable);
      });
    };
    return {
        installEditButtons: installEditButtons};
};
