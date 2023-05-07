$(document).ready(function() {
    $('#form').submit(function(event) {
      event.preventDefault();
  
      var formData = {
        time: $('#time').val(),
        mission: $('#mission').val(),
        goal: $('#goal').val(),
        goal_point: $('#goal-point').val(),
        pleasure_point: $('#pleasure-point').val(),
        notes: $('#notes').val()
      };
      
      $.ajax({
        type: 'POST',
        url: '/form',
        data: JSON.stringify(formData),
        contentType: 'application/json',
        success: function(response) {
          alert(response.response);
          $('#form')[0].reset(); 
        },
        error: function(error) {
          console.log(error);
          alert('An error occurred. Please try again.');
        }
      });
    });
  });
  