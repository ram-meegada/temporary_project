CKEDITOR.on('instanceReady', function (ev) {
    ev.editor.dataProcessor.htmlFilter.addRules({
        elements: {
            span: function (element) {
                if (element.attributes.style) {
                    // Remove only the line-height from styles
                    element.attributes.style = element.attributes.style.replace(/line-height:\s*[^;]+;?/g, '');
                }
            }
        }
    });
});
