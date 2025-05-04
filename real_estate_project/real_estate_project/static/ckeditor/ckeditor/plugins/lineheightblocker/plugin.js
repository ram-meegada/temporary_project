// static/ckeditor/plugins/lineheightblocker/plugin.js
CKEDITOR.plugins.add('lineheightblocker', {
    init: function(editor) {
        editor.on('contentDom', function() {
            editor.document.on('mousedown', function(evt) {
                var styles = editor.document.getBody().getStyle();
                if (styles.lineHeight) {
                    // Remove line-height style from any element
                    editor.document.getBody().removeStyle('line-height');
                }
            });
        });
    }
});
