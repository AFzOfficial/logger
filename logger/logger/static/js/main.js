$('#menu-button').click(function() {
  $('#menu').toggle(200);
});


$(document).click(function(event) {
  var target = $(event.target);
  if (!target.closest('#menu-button').length) {
    $('#menu').hide(200);
  }
});