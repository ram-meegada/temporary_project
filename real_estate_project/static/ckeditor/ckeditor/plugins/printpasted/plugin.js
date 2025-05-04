CKEDITOR.plugins.add('printpaste', {
    init: function (editor) {
        // Listen to the paste event
        editor.on('paste', function (evt) {
            // Get the pasted content
            const pastedData = evt.data.dataValue;

            // Log the pasted content to the console
            console.log('Pasted Content:', pastedData);

            // Optional: You can modify the pasted data if needed
            // evt.data.dataValue = pastedData.replace(/line-height:\s?[\d.]+;/g, '');

            // Notify the user (optional)
            alert('Pasted content has been logged in the console.');
        });
    }
});
