CKEDITOR.on('instanceReady', function (ev) {
    console.log('111111111111111111111111');
    
    ev.editor.on('beforePaste', function(evt) {
        ev.editor.dataProcessor.htmlFilter.addRules({
            elements: {
                $: function (element) {
                    if (element.attributes.style) {
                        element.attributes.style = element.attributes.style.replace(/line-height:\s*[^;]+;?/g, '');
                    }
                }
            }
        });
    });
});

