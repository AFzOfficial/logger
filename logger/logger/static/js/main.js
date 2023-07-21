$('#profile-dropdown-button').click(function () {
  $('#profile-dropdown').toggle(80, 'linear');
});


// $('#menuButton').click(function () {
//   $('#menu').slideToggle(80);
// });


$(document).click(function (event) {
  var target = $(event.target);
  if (!target.closest('#profile-dropdown-button').length) {
    $('#profile-dropdown').hide(80, 'linear');
  }
});

// $(document).click(function (event) {
//   var target = $(event.target);
//   if (!target.closest('#menuButton').length) {
//     $('#menu').slideUp(80);
//   }
// });


$(document).ready(function () {
  var clipboard = new ClipboardJS("#shareProfile");
  clipboard.on("success", function (e) {
    console.info("URL copied to clipboard!");
    e.clearSelection();
  });
  clipboard.on("error", function (e) {
    console.info("Failed to copy URL to clipboard.");
  });
});