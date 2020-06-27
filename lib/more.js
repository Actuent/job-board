$(document).ready(function(){
  $(".more").toggle(function(){
      $(this).text("..less").siblings(".complete").show();
  }, function(){
      $(this).text("more..").siblings(".complete").hide();
  });
});
