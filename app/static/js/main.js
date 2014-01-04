$(document).ready(function(){

	$(".team-select input").change(function(){
    hideShowTeams(this);
  });
    
  //   

	$('.js--all-teams').click(function(e) {
    e.preventDefault();

		$(".team-select input").each(function() {
			$(this).prop('checked', true);
		})

		$('.team').each(function() {
			$(this).slideDown();
		});

	});

  //

  function hideShowTeams(input) {
    var value = input.value;
    var isChecked = input.checked;

    if(isChecked) {
     $(".team"+value).slideDown();
    } else {
     $(".team"+value).slideUp();
    }
  } 

});