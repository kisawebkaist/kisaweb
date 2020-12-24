function readURL(input){if(input.files&&input.files[0]){var reader=new FileReader();reader.onload=function(e){$('#image-preview').attr('src',e.target.result);}
reader.readAsDataURL(input.files[0]);}}
$(function(){$('#image').change(function(){readURL(this);})});;