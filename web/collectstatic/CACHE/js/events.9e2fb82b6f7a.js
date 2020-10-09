$('#register, #deregister').on('click',function(){const $type=$(this).attr('id');$.ajax({type:'POST',url:$(this).attr('data-event-registration-url'),data:{'type':$type,'csrfmiddlewaretoken':CSRF_TOKEN,},success:(response)=>{if(response=='Success'){if($type=='register'){alert($(this).attr('data-event-registration-url'));}
else{}}
else{alert('Error1');}},error:(response)=>{alert('Error0');},});});;