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

//CodeCatalog Snippet http://www.codecatalog.net/244/4/
var edit_description_field = function()
{
	var edit_comment_input = elt('input', { 'type': 'text', 'class': 'edit_description'});
	var edit_description = horizontal(elt('span').text("Edit summary"), edit_comment_input);
	edit_description.val = function(foo) {
		return edit_comment_input.val.apply(edit_comment_input, arguments);
	};
	return edit_description;
};
// End CodeCatalog Snippet

var makeMarkdownArea = function(textarea, divclass, editcallback, custom_on_click){
    var container = elt('div');
    container.addClass(divclass);
    var div = elt('div');
    var markup = textarea.val();
    var converter = new Showdown.converter();

    var editlink = elt('a', {'href':'#'});
    var editdiv = elt('div', {'class':'markdown_edit_div'}, editlink);
    var update = function() { div.html(converter.makeHtml(textarea.val())); };

    var set_edit_text = function() {
        if (textarea.val().length > 0) {
            editlink.text("edit");
            editdiv.removeClass('documentation_editable_empty');
            editdiv.addClass('documentation_editable');
        }
        else {
            editlink.text("add documentation");
            editdiv.addClass('documentation_editable_empty');
            editdiv.removeClass('documentation_editable');
        }
            
    };
    set_edit_text();
    
    // TODO keydown instead to make it more responsive.  Make sure it isn't lagging
    // a character behind though!
    textarea.keyup(update);
    
    editlink.click(function() {
        if (custom_on_click && !custom_on_click()) return;
        editlink.hide();
        pretext = textarea.val();
        textarea.show();

        var edit_description = edit_description_field();

        var savebutton = $('<button>Save</button>');
        savebutton.click(function() {
            set_edit_text();
            editlink.show();
            savebutton.remove();
            cancelbutton.remove();
            edit_description.remove();
            textarea.hide();
            var text = textarea.val();
            if (text != pretext) { editcallback(text, edit_description.val()) }
        });

        var cancelbutton = $('<button>Cancel</button>');
        cancelbutton.click(function() {
            editlink.show();
            savebutton.remove();
            cancelbutton.remove();
            edit_description.remove();
            textarea.val(pretext);
            textarea.hide();
            update();
        });
        textarea.after(edit_description, savebutton, cancelbutton);
        return false;
    });
    container.append(div);
    update();

    textarea.before(container);
    textarea.before(editdiv);
    textarea.hide();
};
