$(document).ready(function(){

	$(".team-select input").change(function(){
		var value = this.value;

		if (!value) return;

		if(this.checked) {
			//alert(value)
			$(".team"+value).slideDown();
		} else {
			$(".team"+value).slideUp();
		}
	});

	$('.js--all-teams').click(function() {
		$(".team-select input").each(function() {
			$(this).prop('checked', true);
		})

		$('.team').each(function() {
			$(this).slideUp();
		})
	});

});