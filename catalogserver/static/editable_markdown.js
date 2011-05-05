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

//CodeCatalog Snippet http://codecatalog.net/244/673/
var edit_description_field = function()
{
	var edit_comment_input = elt('input', { 'type': 'text', 'class': 'edit_description'});
	var edit_description = horizontal(elt('span').text("Edit summary"), edit_comment_input);
	edit_description.val = edit_comment_input.val;
	return edit_description;
};
// End CodeCatalog Snippet

var makeMarkdownArea = function(textarea, divclass, editcallback, custom_on_click){
    var container = $('<div></div>');
    container.addClass(divclass);
    var div = $('<div></div>');
    var markup = textarea.val();
    var converter = new Showdown.converter();

    var editlink = $('<a href="#">edit</a>');
    var update = function() { div.html(converter.makeHtml(textarea.val())); };

    // TODO keydown instead to make it more responsive.  Make sure it isn't lagging
    // a character behind though!
    textarea.keyup(update);
    
    editlink.click(function() {
        if (custom_on_click && !custom_on_click()) return;
        pretext = textarea.val();
        textarea.show();

        var edit_description = edit_description_field();

        var savebutton = $('<button>Save</button>');
        savebutton.click(function() {
            savebutton.remove();
            cancelbutton.remove();
            edit_description.remove();
            textarea.hide();
            var text = textarea.val();
            if (text != pretext) { editcallback(text, edit_description.val()) }
        });

        var cancelbutton = $('<button>Cancel</button>');
        cancelbutton.click(function() {
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
    container.append(editlink);
    update();

    textarea.before(container);
    textarea.hide();
};
