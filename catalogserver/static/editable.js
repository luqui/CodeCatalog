// settings: { editurl, csrf_token }
// Adds a little blue "edit" link next to every element with class .editable.
// If it also has class .editarea, the edit box will be a textarea instead of a
// text input.
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
        var span = $('<div/>');
        var elt = proto.clone();
        var editlink = $('<a href="#" class="dynamic_link">edit</a>');
        span.append(elt).append(editlink);

        editlink.click(function() {
            if (settings.custom_on_click && !settings.custom_on_click()) return;
            span.replaceWith(makeEditBox(elt));
            return false;
        });
        return span;
    };
    var installEditButtons = function() {
      $('.editable').each(function(x,e) { 
        var je = $(e);
        var elt = makeLinkTag(je);
        je.replaceWith(elt);
      });
    };
    return {
        installEditButtons: installEditButtons};
};
