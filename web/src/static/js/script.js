window.addEventListener('load', function () {
    $('#sign-out').onclick = signOut;

    $('#file-input').on('change', function (ev) {
        hideDuplicateWarning();
        showLoadingState();

        const reader = new FileReader();
        reader.readAsArrayBuffer(this.files[0]);
        reader.onload = () => {
            $.post('/check-duplicate', { hash: SparkMD5.ArrayBuffer.hash(reader.result) } )
                .done(function(data) {
                    if (data.duplicate === true) {
                        showDuplicateWarning();
                    }
                })
                .always(() => {
                    hideLoadingState();
                })
        }
        reader.onerror = error => {
            hideLoadingState();
            console.error(error);
        };
    });
});

function showLoadingState() {
    var btn = $('#submit');
    btn.attr('disabled', true);
    btn.html('<i class="icon-spinner icon-spin icon-large"></i> Analyzing image...');
}

function hideLoadingState() {
    var btn = $('#submit');
    btn.attr('disabled', false);
    btn.html('Upload');
}

function hideDuplicateWarning() {
    $('#duplicate-warning')[0].style.display = 'none';
}

function showDuplicateWarning() {
    $('#duplicate-warning')[0].style.display = 'block';
}
