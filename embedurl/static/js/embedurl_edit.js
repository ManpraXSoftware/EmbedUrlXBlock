/* Javascript for pdfXBlock. */
function embedurlXBlockInitEdit(runtime, element) {

    $(element).find('.action-cancel').bind('click', function() {
        runtime.notify('cancel', {});
    });

    $(element).find('.action-save').bind('click', function() {
        var data = {
            'display_name': $('#pdf_edit_display_name').val(),
            'url': $('#pdf_edit_url').val(),
            'new_window_button': $('#pdf_edit_allow_download').val(),
            'min_height': $('#pdf_edit_source_text').val()
        };
        
        runtime.notify('save', {state: 'start'});
        
        var handlerUrl = runtime.handlerUrl(element, 'save_pdf');
        $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
            if (response.result === 'success') {
                runtime.notify('save', {state: 'end'});
                // Reload the whole page :
                // window.location.reload(false);
            } else {
                runtime.notify('error', {msg: response.message})
            }
        });
    });
}
