$(document).ready(function(){

	$(".team-select input").change(function(){
       var value = this.value;
       //alert(value)
       if(this.checked)
       {
         //alert(value)
         $(".team"+value).slideDown();
       }
       else
       {
         $(".team"+value).slideUp();
       }
     })

	$('.jsallteams').click(function() {
		$(".team-select input").each(function() {
			$(this).prop('checked', true);
		})

		$('.team').each(function() {
			$(this).slideUp();
		})
	});

});