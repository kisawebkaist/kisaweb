$('.readmore').on('click', function() {
    $(this).parent().hide();
    $input = $(this).parent().siblings('.descr_truncate_num').children(input_selector);
    $input.val($input.attr('max'));
    get_truncated_text($input);
    $input.val(input_init_val);
    $(this).parent().siblings('.read-less').show();
});

$('.readless').on('click', function() {
    $(this).parent().hide();
    $input = $(this).parent().siblings('.descr_truncate_num').children(input_selector);
    $input.val(input_init_val);
    get_truncated_text($input);
    $(this).parent().siblings('.read-more').show();
});
