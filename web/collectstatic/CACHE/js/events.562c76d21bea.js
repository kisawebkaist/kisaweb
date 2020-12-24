$('#register, #deregister').on('click',function(){const $type=$(this).attr('id');$.ajax({type:'POST',url:$(this).attr('data-event-registration-url'),data:{'type':$type,'csrfmiddlewaretoken':CSRF_TOKEN,},success:function(response){if(response=='Success'){if($type=='register'){alert($(this).hasClass('btn-success'));}
else{}}
else{alert('Error1');}},error:function(response){alert('Error0');},});});;