$(document).ready(function () {
    // Live search using jQuery
    $('#search-input').on('input', function () {
        var query = $(this).val().toLowerCase();
        $('#search-results li').each(function () {
            var text = $(this).text().toLowerCase();
            if (text.indexOf(query) === -1) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    });
});

document.getElementById('fetch-countries-button').addEventListener('click', function() {
    this.innerText = 'Fetching...';
});