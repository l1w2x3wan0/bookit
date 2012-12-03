function get_location(href){
	var l = document.createElement('a');
    l.href = href;
    return l;
}

function set_bookinfo(book){
	$('div#title').html('<a href="'+'show?bookid='+book.douban_bookid+'" target="_blank">'+book.douban_title+'</a>');
	$('div#image').html('<img src="'+book.douban_image+'"/>');
}

function clear_bookinfo(){
	$('div#title').html('');
	$('div#image').html('');
}

$(document).ready(function(){
	$('input#add_btn').click(function(event){
		var bookurl=$('input#douban_bookurl').val();
		$.getJSON('../book/add?url='+encodeURIComponent(bookurl),function(data){
			if(0==data.ret){
				$('div#add_retmsg').text(data.msg);
				$.getJSON('../book/get?id='+data.bookid,set_bookinfo);
			}
			else{
				$('div#add_retmsg').text(data.msg);
				clear_bookinfo();
			}
		});
	});
	
	$('input#import_doulist_btn').click(function(event){
		var url=$('input#douban_doulist').val();
		$.getJSON('../book/importdoulist?url='+encodeURIComponent(url),function(data){
			$('div#import_retmsg').text(data.msg);
		});
	});
});
