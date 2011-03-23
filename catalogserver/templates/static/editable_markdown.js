var makeMarkdownArea = function(textarea, divclass, editcallback){
    var div = $('<div></div>');
    div.addClass(divclass);
    var markup = textarea.val();
    var converter = new Showdown.converter();

    var editlink = $('<a href="#">edit</a>');
    var update = function() { div.html(converter.makeHtml(textarea.val())); div.append(editlink); };

    // TODO keydown instead to make it more responsive.  Make sure it isn't lagging
    // a character behind though!
    textarea.keyup(update);
    
    editlink.click(function() {
        textarea.show();

        var savebutton = $('<button>Save</button>');
        savebutton.click(function() {
            savebutton.remove();
            textarea.hide();
            editcallback(textarea.val());
        });
        textarea.after(savebutton);
    });
    update();
    div.append(editlink);

    textarea.before(div);
    textarea.hide();
};
