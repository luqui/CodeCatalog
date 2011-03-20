var makeMarkdownArea = function(textarea, divclass, editcallback){
    var div = $('<div></div>');
    div.addClass(divclass);
    var markup = textarea.val();
    var converter = new Showdown.converter();
    var html = converter.makeHtml(markup);
    div.append($(html));
    
    var editlink = $('<a href="#">edit</a>');
    editlink.click(function() {
        var newtextarea = $('<textarea rows="15" cols="72"></textarea>');
        newtextarea.val(markup);
        div.replaceWith(newtextarea);

        var savebutton = $('<button>Save</button>');
        savebutton.click(function() {
            savebutton.remove();
            editcallback(newtextarea.val());
            makeMarkdownArea(newtextarea, divclass, editcallback);
        });
        newtextarea.after(savebutton);
    });
    div.append(editlink);

    textarea.replaceWith(div);
};
