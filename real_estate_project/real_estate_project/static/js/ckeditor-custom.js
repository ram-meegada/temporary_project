// CKEDITOR.on('instanceReady', function (ev) {
//     ev.editor.on('beforePaste', function(evt) {
//         ev.editor.dataProcessor.htmlFilter.addRules({
//             elements: {
//                 $: function (element) {
//                     if (element.attributes.style) {
//                         element.attributes.style = element.attributes.style.replace(/line-height:\s*[^;]+;?/g, '');
//                     }
//                 }
//             }
//         });
//     });
// });

CKEDITOR.editorConfig = function (config) {
    console.log('2222222222222222222');
    
    config.allowedContent = {
        $1: {
            elements: CKEDITOR.dtd,
            attributes: true,
            styles: true,
            classes: true
        }
    };
    // config.disallowedContent = '*{line-height}';
};

