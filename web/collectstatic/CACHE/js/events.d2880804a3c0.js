function readURL(input,$preview){if(input.files&&input.files[0]){var reader=new FileReader();reader.onload=function(e){$preview.attr('src',e.target.result);}
reader.readAsDataURL(input.files[0]);}}
$(function(){$event_image_preview=$('#image_preview');height_id='#id_image_height';width_id='#id_image_width';$height=$(height_id);$width=$(width_id);$('#image').change(function(){readURL(this,$event_image_preview);});$('#id_image_contains_information').on('click',function(){$div_id=$('#image_contains_info_dimensions');if($(this).prop('checked')){$div_id.show();}
else{$height.val($height.attr('value'));$width.val($width.attr('value'));$event_image_preview.height($height.attr('value')).width($width.attr('value'));$div_id.hide();}});$(height_id+', '+width_id).change(function(){$val=$(this).val();if($val<0){alert('Please enter a positive integer');$(this).val($(this).attr('value'));}
else{$val-=2;if($(this).attr('id')==height_id){$event_image_preview.height($val);}
else{$event_image_preview.width($val);}}});$('#image_dim_reset').on('click',function(){$height.val($height.attr('value'));$width.val($width.attr('value'));});});;