$(function(){$instance=undefined;$('.register').on('click',function(){$(this).parent().parent().children('.register-form').show();$(this).hide();$(this).parent().children('.register-cancel').show();instance=$(this);f=$(this).parent().parent().children('.register-form').children('.register-form-iframe');console.log(f.contents().children().attr('class'));});$('.register-cancel').on('click',function(){$(this).parent().parent().children('.register-form').hide();$(this).hide();$(this).parent().children('.register').show();});$('.register-form-iframe').on('load',function(){f=$(this)
console.log(f.contents().children('span:contains("Submit")').length);});});;input_selector='input[name="truncate_num"]';input_init_val=$(input_selector).attr('value');edit_selector='.edit';edit_mode_selector='.edit_mode';cancel_selector='.cancel';max_selector='.max';save_selector='.save';event_description_selector='.event-description';read_more_selector='.read-more';function get_input_selector($this){return $this.parent().siblings(input_selector);}
function get_truncated_text($input){max=parseInt($input.attr('max'));value=parseInt($input.val());$.ajax({type:'POST',url:$input.attr('data-modify-truncated-descr-url'),data:{'num':value,'csrfmiddlewaretoken':CSRF_TOKEN,},success:(response)=>{if(response){$input.parent().siblings(event_description_selector).html(response);$read_more=$input.parent().siblings(read_more_selector);if(max>value&&value>=parseInt($input.attr('min'))){$read_more.show();}
else{$read_more.hide();}}},error:()=>{alert('Error');},});}
$(edit_selector).on('click',function(){$(this).hide();$(this).siblings(edit_mode_selector).show();$(this).siblings(input_selector).prop('disabled',false);});$(cancel_selector).on('click',function(){$(this).parent().hide();$(this).parent().siblings(edit_selector).show();$input=get_input_selector($(this));$input.val(input_init_val).prop('disabled',true);get_truncated_text($input);});$(input_selector).change(function(){if(parseInt($(this).val())<parseInt($(this).attr('min'))){$(this).val($(this).attr('min'));}
get_truncated_text($(this));});$(max_selector).on('click',function(){$input=get_input_selector($(this));$input.val($input.attr('max'));get_truncated_text($input);});$(save_selector).on('click',function(){$input=get_input_selector($(this));$.ajax({type:'POST',url:$(this).attr('data-modify-truncate-num-url'),data:{'num':parseInt($input.val()),'csrfmiddlewaretoken':CSRF_TOKEN,},success:(response)=>{if(response=='Success'){$(this).parent().hide();$(this).parent().siblings(edit_selector).show()
$input.prop('disabled',true);}},error:()=>{alert('Error');},});});;$('.readmore').on('click',function(){$(this).parent().hide();$input=$(this).parent().siblings('.descr_truncate_num').children(input_selector);$input.val($input.attr('max'));get_truncated_text($input);$input.val(input_init_val);$(this).parent().siblings('.read-less').show();});$('.readless').on('click',function(){$(this).parent().hide();$input=$(this).parent().siblings('.descr_truncate_num').children(input_selector);$input.val(input_init_val);get_truncated_text($input);$(this).parent().siblings('.read-more').show();});;