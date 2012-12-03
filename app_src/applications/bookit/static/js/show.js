function set_count(data){
	$('div#total').html(data.total);
	$('div#available').html(data.available);
};

$(document).ready(function(){
	$('input#checkinby1').click(function(){
		$(this).attr("disabled",true); 
		var id=$('div#id').html();
		$.getJSON('../book/checkin?id='+id+'&count=1',function(data){
			$('input#checkinby1').attr("disabled",false); 
			if(data)
				set_count(data);
		});
	});
	$('input#checkoutby1').click(function(){
		$(this).attr("disabled",true); 
		var id=$('div#id').html();
		$.getJSON('../book/checkout?id='+id+'&count=1',function(data){
			$('input#checkoutby1').attr("disabled",false); 
			if(data)
				set_count(data);
		});
	});
	$('input#borrow').click(function(){
		
	});
});
