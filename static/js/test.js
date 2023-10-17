
function myfunction(){
  let bttn = document.getElementById("btn1");
  alert("HELLO mia vaiasdasdad");
}

$(document).ready(function() {
    $('.edit-task').click(function() {
        var taskId = $(this).data('task-id');
        $.ajax({
            url: '/get_task_details/' + taskId + '/',
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                $('#taskIds').val(data.id);
                $('#taskName').val(data.name);
                $('#taskDate').val(data.date);
                $('#taskClient').val(data.client)
                $('#taskStatus').val(data.status);
                $('#taskTime').val(data.time);
  
            },
            error: function() {
                // Handle error
            }
        });
    });
  
    $('#saveChanges').click(function() {
        var taskId = $('#taskIds').val();
        console.log(taskId)
        var taskName = $('#taskName').val();
        var taskDate = $('#taskDate').val();
        var taskStatus = $('#taskStatus').val();
        var taskTime = $('#taskTime').val();
        $.ajax({
            url: '/update_task/' + taskId + '/',
            type: 'POST',
            cache: false,
            data: {
                task_name: taskName,
                date: taskDate,
                status: taskStatus,
                time: taskTime,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(data) {
                $('#exampleModal').modal('hide');
                $('.modal-backdrop').remove();
  
                location.reload();
  
                // Update the table or display a success message
            },
            error: function() {
                // Handle error
            }
        });
    });
  });
