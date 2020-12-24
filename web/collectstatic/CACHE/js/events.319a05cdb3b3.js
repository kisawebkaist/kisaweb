function readURL(input,$preview){if(input.files&&input.files[0]){var reader=new FileReader();reader.onload=function(e){$preview.attr('src',e.target.result);}
reader.readAsDataURL(input.files[0]);}}
$(function(){$event_image_preview=$('#image_preview');$('#image').change(function(){readURL(this,$event_image_preview);});$('#id_image_contains_information').on('click',function(){$div_id=$('#image_contains_info_dimensions');if($(this).prop('checked')){$div_id.show();}
else{$height=$('#id_image_height');$width=$('#id_image_width');$height.val($height.attr('value'));$width.val($width.attr('value'));$event_image_preview.height($height.attr('value')).width($width.attr('value'));$div_id.hide();}});$('#id_image_height, #id_image_width').change(function(){$val=$(this).val();if($val<0){alert('Please enter a positive integer');$(this).val($(this).attr('value'));}
else{$val-=2;if($(this).attr('id')=='id_image_height'){$event_image_preview.height($val);}
else{$event_image_preview.width($val);}}});});;