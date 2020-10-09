$event_image_preview=$('#image_preview');function readURL(input){if(input.files&&input.files[0]){var reader=new FileReader();reader.onload=function(e){$event_image_preview.attr('src',e.target.result);}
reader.readAsDataURL(input.files[0]);}}
$(function(){$('#image').change(function(){readURL(this);});$('#id_image_contains_information').on('click',function(){$div_id=$('#image_contains_info_dimensions');if($(this).prop('checked')){$div_id.show();}
else{$div_id.hide();}});$('#id_image_height').change(function(){alert($('#id_image_height').val());});});;