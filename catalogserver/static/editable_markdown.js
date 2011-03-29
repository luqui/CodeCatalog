var makeMarkdownArea = function(textarea, divclass, editcallback){
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
        pretext = textarea.val();
        textarea.show();

        var savebutton = $('<button>Save</button>');
        savebutton.click(function() {
            savebutton.remove();
            cancelbutton.remove()
            textarea.hide();
            var text = textarea.val();
            if (text != pretext) { editcallback(text) }
        });

        var cancelbutton = $('<button>Cancel</button>');
        cancelbutton.click(function() {
            savebutton.remove();
            cancelbutton.remove();
            textarea.val(pretext);
            textarea.hide();
            update();
        });
        textarea.after(savebutton, cancelbutton);
        return false;
    });
    container.append(div);
    container.append(editlink);
    update();

    textarea.before(container);
    textarea.hide();
};
