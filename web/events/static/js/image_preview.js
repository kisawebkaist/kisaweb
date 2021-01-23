// Script used in event_form.html

function readURL(input, $preview) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            $preview.attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
    }
}

$(function() {
    $image_preview = $('#image_preview');
    height_id = '#id_image_height';
    width_id = '#id_image_width';
    $height = $(height_id);
    $width = $(width_id);
    height_default = $height.attr('value');
    width_default = $width.attr('value');
    $image_dim_reset = $('#image_dim_reset');

    $('#reset-id-reset').on("click", () => {
        // getting the currently uploaded image (used for Update View)
        currently = $("span[class='text-break']"); 
        if(currently.length > 0) { // if UpdateView
            normal_img_link = $(currently[0].getElementsByTagName('a')[0]).attr('href');
            $image_preview.attr('src', normal_img_link);
        }
        else { // if CreateView
            $image_preview.attr('src', '/static/img/events-default-dev-dist.png');
        }
        $("label[for='image']")[1].textContent = '---';
    });

    $('#image').change(function() {
        readURL(this, $image_preview);
    });

    $('#id_custom_image_dimensions').on('click', function() {
        if ($(this).prop('checked')) {
            $height.prop('disabled', false);
            $width.prop('disabled', false)
            $image_dim_reset.show();
        }
        else {
            $height.val($height.attr('value')).prop('disabled', true);
            $width.val($width.attr('value')).prop('disabled', true);
            $image_preview.height(height_default).width(width_default);
            $image_dim_reset.hide();
        }
    });

    $(height_id + ', ' + width_id).change(function() {
        $val = $(this).val();
        if ($val < 0) {
            alert('Please enter a positive integer');
            $(this).val($(this).attr('value'));
        }
        else {
            $val -= 2; // For some reason the value kept getting incremented by 2.
            if ($(this).attr('id') == height_id.substring(1)) {
                $image_preview.height($val);
            }
            else {
                $image_preview.width($val);
            }
        }
    });

    $image_dim_reset.on('click', function() {
        $height.val(height_default);
        $width.val(width_default);
        $image_preview.height(height_default).width(width_default);
    });
});
