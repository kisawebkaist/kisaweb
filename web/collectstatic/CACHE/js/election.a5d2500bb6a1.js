$(function(){$('.vote-single').on('click',function(){var vote_type=$(this).val();if(confirm(`Are you sure you want to vote ${vote_type.toUpperCase()} for this candidate?`)){$.ajax({type:'POST',url:$(this).attr('data-url'),data:{'type':vote_type,'csrfmiddlewaretoken':CSRF_TOKEN,},success:(response)=>{if(response=='novote'){alert('It is not the voting period.');location.reload();}
else if(response=='Success'){location.reload();}},error:()=>{alert('Error');},});}});});;$(function(){var oldval;$('.ratio-select').on('focus',function(){oldval=$(this).val();}).on('change',function(){$.ajax({type:'POST',url:$(this).attr('data-embed-ratio-url'),data:{'ratio':$(this).val(),'csrfmiddlewaretoken':CSRF_TOKEN,},success:(response)=>{if(response=='Success'){let oldclass=`embed-responsive-${ oldval }`;let newclass=`embed-responsive-${ $(this).val() }`;$('.embed-responsive').removeClass(oldclass).addClass(newclass);}
else{alert('Error1');}},error:()=>{alert('Error0');},});});});;