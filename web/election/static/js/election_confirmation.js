// Enable/disable voting buttons until user confirms non-Korean passport
$(function() {
    var $checkbox = $('#non-korean-confirmation');

    function updateButtons() {
        var checked = $checkbox.is(':checked');
        $('.requires-confirmation').each(function() {
            var $btn = $(this);
            // store initial disabled state on first check
            if ($btn.data('initial-disabled') === undefined) {
                $btn.data('initial-disabled', $btn.prop('disabled'));
            }
            // if it was initially disabled by the server, leave it disabled
            if ($btn.data('initial-disabled')) {
                return;
            }
            $btn.prop('disabled', !checked);
        });
    }

    // Only bind if checkbox exists on the page
    if ($checkbox.length) {
        $checkbox.on('change', updateButtons);
        // initialize state on page load
        updateButtons();
    }
});
